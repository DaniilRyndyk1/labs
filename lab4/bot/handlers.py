import validators

from utility import *
from constants import *

from database import Database
import channel_parser

from telegram import KeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, ConversationHandler

database = Database()

async def show_settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global database
    current_id = update.effective_user.id

    if not database.is_admin(current_id):
        await update.message.reply_text(text="Только администратор может менять настройки")
        return END

    text = "Добро пожаловать в меню изменения настроек"

    keyboard = get_settings_keyboard()

    await update.message.reply_text(text=text, reply_markup=keyboard)

    return SELECTING_ITEM
        

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global database
    url = database.get_channel_url()

    text = "Вы успешно зарегистрированы в системе"

    keyboard = await get_main_keyboard(url)

    await update.message.reply_text(text=text, reply_markup=keyboard)

    return SELECTING_ITEM


async def show_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    global database

    url = database.get_channel_url()
    text = f"Ссылка на текущий канал: {'отсутствует' if url == '' else url}"

    keyboard = ReplyKeyboardMarkup([["Назад"]], resize_keyboard=True)

    await update.message.reply_text(text=text, reply_markup=keyboard)
    # await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return BACK

async def change_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = ReplyKeyboardMarkup([["Назад"]], resize_keyboard=True)

    await update.message.reply_text(text="Введите URL канала", reply_markup=keyboard)
    return TYPING

async def change_url_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global database
    url = update.message.text
    user_id = update.effective_user.id
    action = END

    if url == "Назад":
        await show_settings_menu(update, context)
        return END

    if url is None or url == "":
        text = "Введите ссылку на канал"
        action = TYPING

    elif not validators.url(url):
        text = "Введенное значение не является ссылкой"
        action = TYPING

    elif not database.exists(user_id):
        text = "Введите /start для регистрации в системе"

    elif database.is_admin(user_id):
        database.set_channel_url(url)
        text = "Url канала для комментирования успешно обновлен"

    else:
        text = "Нет прав"

    await update.message.reply_text(text)
    await show_settings_menu(update, context)
    return action

async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = ReplyKeyboardMarkup([["Назад"]], resize_keyboard=True)

    await update.message.reply_text(text="Введите id пользователя", reply_markup=keyboard)
    return TYPING

async def add_admin_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global database

    user_id = update.message.text
    current_id = update.effective_user.id
    action = END

    if user_id == "Назад":
        await show_settings_menu(update, context)
        return END

    if user_id is None or user_id == "":
        text = "Введите id пользователя"
        action = TYPING

    elif not user_id.isdigit():
        text = "Введен неправильный id - он может состоять только из чисел"
        action = TYPING

    elif not database.exists(current_id):
        text = "Введите /start для регистрации в системе"

    elif database.is_admin(current_id):
        user_id = int(user_id)

        if not database.exists(user_id):
            text = "Пользователь не существует"
            action = TYPING

        elif database.is_admin(user_id):
            text = "Пользователь уже является админом"

        else:
            database.set_admin(user_id)
            text = "Новый администратор успешно добавлен"
    else:
        text = "Нет прав"

    await update.message.reply_text(text)
    await show_settings_menu(update, context)
    return action

async def remove_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = ReplyKeyboardMarkup([["Назад"]], resize_keyboard=True)

    await update.message.reply_text(text="Введите id пользователя", reply_markup=keyboard)
    return TYPING

async def show_posts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global database
    await update.message.reply_text("Загружаем посты...")
    channel = database.get_channel_url()
    channel = channel[channel.rfind('/')+1:]
    posts = await channel_parser.get_history(channel)
    for post in posts:
        if post['text'] != '':
            url = f"https://daniilryndyk1.github.io/testtest?url={channel}&postId={post['id']}"
            print(url)
            # web_app = WebAppInfo(url)
            button = InlineKeyboardButton(text="Прокомментировать", url=url)
            keyboard = InlineKeyboardMarkup([[button]])
            await update.message.reply_text(text=f"{post['text']}", reply_markup=keyboard)
    return SELECTING_ITEM

async def remove_admin_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global database

    user_id = update.message.text
    current_id = update.effective_user.id
    action = END

    if user_id == "Назад":
        await show_settings_menu(update, context)
        return END

    if user_id is None or user_id == "":
        text = "Введите id администратора"
        action = TYPING

    elif not user_id.isdigit():
        text = "Введен неправильный id - он может состоять только из чисел"
        action = TYPING

    elif not database.exists(current_id):
        text = "Введите /start для регистрации в системе"

    elif database.is_admin(current_id):
        user_id = int(user_id)

        if not database.exists(user_id):
            text = "Пользователь не существует"
            action = TYPING

        elif not database.can_be_removed(user_id):
            text = "Пользователь защищен от изменений" 

        elif not database.is_admin(current_id):
            text = "Введен id пользователя, который не является администратором"
            action = TYPING

        else:
            database.remove_admin(user_id)
            text = "Администратор успешно удален"

    else:
        text = "Нет прав"

    await update.message.reply_text(text)
    await show_settings_menu(update, context)
    return action

# async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
#     return BACK

async def show_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    current_id = update.effective_user.id
    await update.message.reply_text(text=f"Ваш id: {current_id}")
    await show_settings_menu(update, context)
    return END

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text(text="Команда принудительно завершена")
    return STOPPING

async def show_app(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text(text="Команда принудительно завершена")
    return STOPPING

async def end_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global database
    url = database.get_channel_url()
    await update.message.reply_text(text="Редактирование настроек завершено", reply_markup=await get_main_keyboard(url))
    # await update.callback_query.answer()
    # await update.callback_query.edit_message_text("Редактирование настроек успешно завершено")
    return END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(text="Бот отключен", reply_markup=ReplyKeyboardRemove())
    # await update.callback_query.answer()
    # await update.callback_query.edit_message_text("Редактирование настроек успешно завершено")
    return END