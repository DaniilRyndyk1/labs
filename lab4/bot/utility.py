from telegram import ReplyKeyboardMarkup

def get_settings_keyboard():
    buttons = [
        [
            "Добавить админа",
            "Удалить админа",
        ],
        [
            "Посмотреть канал",
            "Изменить канал",
        ],
        [
            "Посмотреть мой id",
        ],
        [
            "Назад"
        ]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def get_main_keyboard():
    buttons = [
        [
            "Посмотреть последние посты"
        ],
        [
            "Настройки",
        ],
        [
            "Выход"
        ]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def get_empty_keyboard():
    buttons = [
        [
            ""
        ]
    ]

    return ReplyKeyboardMarkup(buttons, is_persistent=True, resize_keyboard=True)