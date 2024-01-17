from telegram.ext import ConversationHandler

(
    SELECTING_ITEM,
    ADD_ADMIN,
    REMOVE_ADMIN,
    SELECTING_URL,
    TYPING,
    STOPPING,
    SHOWING_URL,
    START_OVER,
    CHANGE_URL,
    SHOWING_MENU,
    BACK,
    SETTINGS
) = map(chr, range(10, 22))

END = ConversationHandler.END