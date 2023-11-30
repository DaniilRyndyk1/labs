

class User(object):
    def __init__(self, id: int, removable: bool = True) -> None:
        self.id = id
        self.__is_admin = False
        self.__is_removable = removable

    def can_be_removed(self) -> bool:
        return self.__is_removable

    def is_admin(self) -> bool:
        return self.__is_admin

    def set_admin(self) -> None:
        self.__is_admin = True