import logging

from warnings import filterwarnings
from handlers import *

from telegram.warnings import PTBUserWarning

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler

TOKEN = "6824033913:AAESU0MjjEmWO_3IyobafCwZDXRZw0zwOsw"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

def main():
    application = Application.builder().token(TOKEN).build()

    remove_admin_conversation = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Text('Удалить админа'), remove_admin),
        ],
        states={
            TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_admin_input)],
        },
        fallbacks=[
            CommandHandler("stop", stop),
            MessageHandler(filters.Text('Назад'), show_settings_menu)
        ],
        map_to_parent={
            END: SHOWING_MENU,
            STOPPING: SHOWING_MENU,
        },
    )

    change_url_conversation = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Text('Изменить канал'), change_url),
        ],
        states={
            TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_url_input)],
        },
        fallbacks=[
            CommandHandler("stop", stop)
        ],
        map_to_parent={
            END: SHOWING_MENU,
            STOPPING: SHOWING_MENU,
        },
    )

    add_admin_conversation = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Text('Добавить админа'), add_admin),
        ],
        states={
            TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_admin_input)]
        },
        fallbacks=[
            CommandHandler("stop", stop),
            MessageHandler(filters.Text('Назад'), show_settings_menu)
        ],
        map_to_parent={
            END: SHOWING_MENU,
            STOPPING: SHOWING_MENU,
        },
    )

    settings_conversation = ConversationHandler(
        entry_points=[MessageHandler(filters.Text('Настройки'), show_settings_menu)],
        states={
            SELECTING_ITEM: [
                add_admin_conversation,
                remove_admin_conversation, 
                change_url_conversation,
                MessageHandler(filters.Text('Посмотреть канал'), show_url),
                MessageHandler(filters.Text('Посмотреть мой id'), show_id),
            ],
            BACK: [MessageHandler(filters.Text('Назад'), show_settings_menu)]
        },
        fallbacks=[
            CommandHandler("stop", stop),
            MessageHandler(filters.Text('Назад'), end_settings)
        ],
        map_to_parent={
            END: SELECTING_ITEM
        },
    )

    main_conversation = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_ITEM: [
                settings_conversation,
                MessageHandler(filters.Text('Посмотреть последние посты'), show_posts),
                MessageHandler(filters.Text('Назад'), end_settings),
                MessageHandler(filters.Text('Выход'), end)
            ],
            BACK: [MessageHandler(filters.Text('Назад'), show_settings_menu)]
        },
        fallbacks=[
            CommandHandler("stop", stop)
        ]
    )

    application.add_handler(main_conversation)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()