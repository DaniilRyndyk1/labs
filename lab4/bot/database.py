import sqlite3

from user import User

USERS_TABLE_NAME = "users"
META_TABLE_NAME = "meta"
CHANNEL_URL_COLLUMN_NAME = "CHANNEL_URL"
ADMIN_USER_ID = [
    1832921877,
    310519888
]

class Database():

    def __init__(self) -> None: 
        self.__connection = sqlite3.connect("users.db")

        cursor = self.__connection.cursor()
        self.__cursor = cursor

        # создание таблицы пользователей
        cursor.execute(f'''SELECT name 
                           FROM sqlite_master 
                           WHERE type='table' AND name = '{USERS_TABLE_NAME}' ''')
        result = cursor.fetchone()
        if result == None:
            cursor.execute("CREATE TABLE users(id INT, is_admin BOOLEAN, can_be_removed BOOLEAN)")
            for id in ADMIN_USER_ID:
                user = User(id, False)
                user.set_admin()
                self.save_user(user)

        # создание таблицы с настройками бота
        cursor.execute(f'''SELECT name
                           FROM sqlite_master
                           WHERE type='table' AND name = '{META_TABLE_NAME}' ''')
        result = cursor.fetchone()
        if result == None:
            cursor.execute(f"CREATE TABLE {META_TABLE_NAME}(name TEXT, value TEXT)")
            self.__connection.execute(f'''INSERT INTO {META_TABLE_NAME} 
                                          VALUES ('{CHANNEL_URL_COLLUMN_NAME}', '')''')
            self.__connection.commit()

    def exists(self, id: int) -> bool:
        self.__cursor.execute(f'''SELECT COUNT(id) 
                                  FROM {USERS_TABLE_NAME} 
                                  WHERE id={id}''')
        result = self.__cursor.fetchone()
        return result[0] > 0
    
    def is_admin(self, id: int) -> bool:
        self.__cursor.execute(f'''SELECT is_admin = TRUE 
                                  FROM {USERS_TABLE_NAME} 
                                  WHERE id={id}''')
        result = self.__cursor.fetchone()

        if result is None:
            return False

        return result[0]
    
    def can_be_removed(self, id: int) -> bool:
        self.__cursor.execute(f'''SELECT can_be_removed = TRUE 
                                  FROM {USERS_TABLE_NAME} 
                                  WHERE id={id}''')
        result = self.__cursor.fetchone()

        if result is None:
            return False

        return result[0]

    def get_user_by_id(self, id: int) -> User:
        self.__cursor.execute(f'''SELECT * 
                                  FROM {USERS_TABLE_NAME} 
                                  WHERE id={id}''')
        result = self.__cursor.fetchone()
        id = result[0]
        can_be_removed = bool(result[2])
        
        user = User(id, can_be_removed)
        
        is_admin = bool(result[1])
        if is_admin:
            user.set_admin()
        
        return user

    def save_user(self, user: User) -> None:
        if self.exists(user.id):
            self.__cursor.execute(f'''UPDATE {USERS_TABLE_NAME} 
                                      SET is_admin={user.is_admin()}
                                      WHERE id = {user.id}''')
        else:
            self.__cursor.execute(f'''INSERT INTO {USERS_TABLE_NAME} 
                                      VALUES ({user.id}, {user.is_admin()}, {user.can_be_removed()})''')
        self.__connection.commit()

    def set_channel_url(self, url: str) -> None:
        self.__cursor.execute(f'''UPDATE {META_TABLE_NAME} 
                                  SET value='{url}'
                                  WHERE name = '{CHANNEL_URL_COLLUMN_NAME}' ''')
        self.__connection.commit()

    def get_channel_url(self) -> str:
        self.__cursor.execute(f'''SELECT value 
                                  FROM {META_TABLE_NAME} 
                                  WHERE name = '{CHANNEL_URL_COLLUMN_NAME}' ''')
        return self.__cursor.fetchone()[0]
    
    def set_admin(self, id: int) -> None:
        self.__cursor.execute(f'''UPDATE {USERS_TABLE_NAME} 
                                  SET is_admin=TRUE 
                                  WHERE id={id}''')
        self.__connection.commit()

    def remove_admin(self, id: int) -> None:
        self.__cursor.execute(f'''UPDATE {USERS_TABLE_NAME} 
                                  SET is_admin=FALSE 
                                  WHERE id={id} AND can_be_removed=True''')
        self.__connection.commit()