

class User(object):
    def __init__(self, id: int) -> None:
        self.__id = id
        self.__is_admin = False
        self.channel_url = ""

    def is_admin(self) -> bool:
        return self.__is_admin

    def set_admin(self) -> None:
        self.__is_admin = True