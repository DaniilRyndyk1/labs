import logging
import validators
import sqlite3

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from user import User

TOKEN = "6824033913:AAESU0MjjEmWO_3IyobafCwZDXRZw0zwOsw"



users = []

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Введите /help для получения справки")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global users
    user_id = update.effective_user.id
    if users[user_id]["is_admin"]:
        text = "Вы можете изменить настройки бота: /change_channel для изменения канала для виджета, /add_admin для добавления нового авторизованного пользователя"
    else:
        text = "Нет прав"
    await update.message.reply_text(text)


async def change_channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global settings

    args = context.args

    if len(args) != 1:
        text = "Использование: /change_channel https://t.me/Ryndyk_Daniil_UITIiA_Lab4_Bot"
    elif not validators.url(args[0]):
        text = "Введенное значение не является ссылкой"
    elif update.effective_user.id in settings["admins_users_id"]:
        settings["channel_url"] = args[0]
        print(settings)
        text = "Url канала для комментирования успешно обновлен"
    else:
        text = "Нет прав"
    await update.message.reply_text(text)


async def add_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global settings
    if update.effective_user.id in settings["admins_users_id"]:
        user_id = int(update.message.text)
        settings["admins_users_id"].append(user_id)
        text = "Новый администратор успешно добавлен"
    else:
        text = "Нет прав"
    await update.message.reply_text(text)


def main() -> None:
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE users(id INT, channel_url TEXT, is_admin BOOLEAN)")

    # application = Application.builder().token(TOKEN).build()

    # application.add_handler(CommandHandler("help", help_command))
    # application.add_handler(CommandHandler("change_channel", change_channel_command))
    # application.add_handler(CommandHandler("add_admin", add_admin_command))

    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))

    # application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()