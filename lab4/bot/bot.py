import logging
import validators

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, ConversationHandler

from database import Database

from user import User

TOKEN = "6824033913:AAESU0MjjEmWO_3IyobafCwZDXRZw0zwOsw"

# State definitions for top level conversation
SELECTING_ACTION, ADDING_ADMIN, REMOVE_ADMIN, DESCRIBING_SELF = map(chr, range(4))
# State definitions for second level conversation
SELECTING_LEVEL, SELECTING_URL = map(chr, range(4, 6))
# State definitions for descriptions conversation
SELECTING_FEATURE, TYPING = map(chr, range(6, 8))
# Meta states
STOPPING, SHOWING = map(chr, range(8, 10))
# Shortcut for ConversationHandler.END
END = ConversationHandler.END

# Different constants for this example
(
    PARENTS,
    CHILDREN,
    SELF,
    GENDER,
    MALE,
    FEMALE,
    AGE,
    NAME,
    START_OVER,
    FEATURES,
    CURRENT_FEATURE,
    CURRENT_LEVEL,
) = map(chr, range(10, 22))

database = Database()

users = []

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

start_markup = ReplyKeyboardMarkup([["/help"]], 
                                   one_time_keyboard=True, 
                                   input_field_placeholder="/help")

SETTINGS, CHANGE_URL, ADD_ADMIN, REMOVE_ADMIN, CHANGE_URL_ENTERED, ADD_ADMIN_ENTERED, REMOVE_ADMIN_ENTERED = range(7)

help_markup = ReplyKeyboardMarkup([["Поменять канал", "Добавить администратора", "Удалить администратора"]], 
                                  one_time_keyboard=False, 
                                  input_field_placeholder="/change_channel")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global database, start_markup
    user_id = update.effective_user.id
    if not database.exists(user_id):
        user = User(user_id)
        database.save_user(user)
    await update.message.reply_text("Введите /help для получения справки", reply_markup=start_markup)


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global database, help_markup
    user_id = update.effective_user.id
    if not database.exists(user_id):
        text = "Введите /start для регистрации в системе"
    elif database.is_admin(update.effective_user.id):
        keyboard = [
            [InlineKeyboardButton("Изменить ссылку на канал", callback_data="/change_url")],
            [InlineKeyboardButton("Добавить администратора", callback_data="/add_admin")],
            [InlineKeyboardButton("Удалить администратора", callback_data="/remove_admin")],
            [InlineKeyboardButton("Выйти из меню настроек", callback_data="/exit")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Вы можете изменить настройки бота:", reply_markup=reply_markup)
        # text = '''Вы можете изменить настройки бота:\n
        # /change_channel <ссылка> - изменение ссылки на канал\n
        # /add_admin <id пользователя> - добавить администратора\n
        # /remove_admin <id пользователя> - удалить администратора\n'''
        # await update.message.reply_text(text, reply_markup=help_markup)
    else:
        text = "Нет прав" #TODO добавить команду для просмотра react приложения
        await update.message.reply_text(text)
    
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # query = update.callback_query
    # command = query.data

    text = "Добро пожаловать! В этом боте вы можете выбрать канал (если вы администратор) и прокомментировать любую запись"

    buttons = [
        [
            InlineKeyboardButton(text="Добавить админа", callback_data=str(ADD_ADMIN)),
            InlineKeyboardButton(text="! Удалить админа", callback_data=str(REMOVE_ADMIN)),
        ],
        [
            InlineKeyboardButton(text="Посмотреть канал", callback_data=str(SHOWING)),
            InlineKeyboardButton(text="Закончить редактирование", callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        await update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return SELECTING_ACTION
        
async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Pretty print gathered data."""
    global database

    user_data = context.user_data
    url = database.get_channel_url()
    text = f"Ссылка на текущий канал: {'отстутсвует' if url == '' else url}"

    buttons = [[InlineKeyboardButton(text="Назад", callback_data=str(END))]]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    user_data[START_OVER] = True

    return SHOWING

async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    update.message.reply_text("Изменение настроек завершено")

async def change_channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global database
    query = update.callback_query
    
    await query.answer()
    await query.edit_message_text(text="Введите URL канала")
    return CHANGE_URL_ENTERED

async def change_channel_entered_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global database
    url = update.message.text
    user_id = update.effective_user.id
    result_code = SETTINGS

    if url is None or url == "":
        text = "Введите ссылку на канал"
        result_code = CHANGE_URL_ENTERED
    elif not validators.url(url):
        text = "Введенное значение не является ссылкой"
        result_code = CHANGE_URL_ENTERED
    elif not database.exists(user_id):
        text = "Введите /start для регистрации в системе"
        result_code = ConversationHandler.END
    elif database.is_admin(user_id):
        database.set_channel_url(url)
        text = "Url канала для комментирования успешно обновлен"
    else:
        text = "Нет прав"

    await update.message.reply_text(text)
    return result_code

async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()

    text = "Введите id пользователя"
    await update.callback_query.edit_message_text(text=text)

    return TYPING

async def add_admin_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global database

    user_id = update.message.text
    current_id = update.effective_user.id
    result_code = SETTINGS

    if user_id is None or user_id == "":
        text = "Введите id пользователя"
        result_code = TYPING
    elif not user_id.isdigit():
        text = "Введен неправильный id - он может состоять только из чисел"
        result_code = TYPING
    elif not database.exists(current_id):
        text = "Введите /start для регистрации в системе"
        result_code = END
    elif database.is_admin(current_id):
        user_id = int(user_id)
        if not database.exists(user_id):
            text = "Пользователь не существует"
            result_code = ADD_ADMIN
        elif database.is_admin(user_id):
            text = "Пользователь уже является админом"
        else:
            database.set_admin(user_id)
            text = "Новый администратор успешно добавлен"
    else:
        text = "Нет прав"
        result_code = END

    await update.message.reply_text(text)
    return result_code

async def remove_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global database

    await update.message.reply_text(text="Введите id пользователя")
    return CHANGE_URL_ENTERED

async def remove_admin_entered_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global database

    user_id = update.message.text
    current_id = update.effective_user.id
    result_code = SETTINGS

    if user_id is None or user_id == "":
        text = "Введите id администратора"
        result_code = REMOVE_ADMIN_ENTERED
    elif not user_id.isdigit():
        text = "Введен неправильный id - он может состоять только из чисел"
        result_code = REMOVE_ADMIN_ENTERED
    elif not database.exists(current_id):
        text = "Введите /start для регистрации в системе"
        result_code = ConversationHandler.END
    elif database.is_admin(current_id):
        user_id = int(user_id)

        if not database.exists(user_id):
            text = "Пользователь не существует"
            result_code = REMOVE_ADMIN_ENTERED
        elif not database.can_be_removed(user_id):
            text = "Пользователь защищен от изменений" 
        elif not database.is_admin(current_id):
            text = "Введен id пользователя, который не является администратором"
            result_code = REMOVE_ADMIN_ENTERED
        else:
            database.remove_admin(user_id)
            text = "Администратор успешно удален"
    else:
        text = "Нет прав"
        result_code = ConversationHandler.END
    await update.message.reply_text(text)
    return result_code

async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Save input for feature and return to feature selection."""
    user_data = context.user_data
    user_data[FEATURES][user_data[CURRENT_FEATURE]] = update.message.text

    user_data[START_OVER] = True

    return END

async def stop_nested(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Completely end conversation from within nested conversation."""
    await update.message.reply_text("Команда принудительно завершена")

    return STOPPING

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End conversation from InlineKeyboardButton."""
    await update.callback_query.answer()

    text = "Редактирование настроек успешно завершено"
    await update.callback_query.edit_message_text(text=text)

    return END

def main() -> None:

    application = Application.builder().token(TOKEN).build()

    add_admin_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                add_admin, pattern="^" + str(ADD_ADMIN) + "$"
            )
        ],
        states={
            TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_admin_input)],
        },
        fallbacks=[
            # CallbackQueryHandler(end_describing, pattern="^" + str(END) + "$"),
            CommandHandler("stop", stop_nested),
        ],
        map_to_parent={
            # Return to second level menu
            END: SHOWING,
            # End conversation altogether
            STOPPING: STOPPING,
        },
    )

    # Set up top level ConversationHandler (selecting action)
    # Because the states of the third level conversation map to the ones of the second level
    # conversation, we need to make sure the top level conversation can also handle them
    selection_handlers = [
        add_admin_conv,
        CallbackQueryHandler(show_data, pattern="^" + str(SHOWING) + "$"),
        CallbackQueryHandler(remove_admin, pattern="^" + str(REMOVE_ADMIN) + "$"),
        CallbackQueryHandler(end, pattern="^" + str(END) + "$"),
    ]
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", show_menu)],
        states={
            SHOWING: [CallbackQueryHandler(show_menu, pattern="^" + str(END) + "$")],
            SELECTING_ACTION: selection_handlers,
            # DESCRIBING_SELF: [description_conv],
            # STOPPING: [CommandHandler("start", show_menu)],
        },
        fallbacks=[CommandHandler("stop", exit)],
    )

    application.add_handler(conv_handler)

    # settings_conversation_handler = ConversationHandler(
    #     entry_points=[CommandHandler("settings", settings_command)],
    #     states={
    #         SETTINGS: [settings_command],
    #         CHANGE_URL: [change_channel_command],
    #         CHANGE_URL_ENTERED: [change_channel_entered_command],
    #         ADD_ADMIN: [add_admin],
    #         ADD_ADMIN_ENTERED: [add_admin_command_entered_command],
    #         REMOVE_ADMIN: [remove_admin_command],
    #         REMOVE_ADMIN_ENTERED: [remove_admin_entered_command],
    #     },
    #     fallbacks=[CommandHandler("exit", exit)],
    # )

    # application.add_handler(settings_conversation_handler)
    # application.add_handler(CallbackQueryHandler(show_menu))
    #application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start_command))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()