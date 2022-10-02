import sqlite3 as sql
from tkinter.messagebox import RETRY

class Connector:

    __cursor = None
    __db = None

    def __init__(self):
        with sql.connect('forum.db') as db:
            self.__cursor = db.cursor()
            self.__db = db
            
            self.__create_user_roles__()
            self.__create_users__()
            self.__create_topic_types__()
            self.__create_topics__()
            self.__create_users__()
            self.__create_messages__()
    
    def __create_user_roles__(self):
        self.__cursor.execute(
            """
            CREATE TABLE if not exists UserRoles(
                id INTEGER PRIMARY KEY,
                name TEXT
            )
            """
        )

        self.__db.commit()
        
    def __create_users__(self):
        self.__cursor.execute(
            """
            CREATE TABLE if not exists Users(
                id INTEGER PRIMARY KEY,
                user_name TEXT,
                password TEXT,
                role INTEGER,
                FOREIGN KEY (role) REFERENCES UserRoles (id) 
            )
            """
        )

        self.__db.commit()

    def __create_topic_types__(self):
        self.__cursor.execute(
            """
            CREATE TABLE if not exists TopicTypes(
                id INTEGER PRIMARY KEY,
                author INTEGER,
                create_date DATE,
                create_time TIME,
                name TEXT,
                FOREIGN KEY (author) REFERENCES Users (id) 
            )
            """
        )

        self.__db.commit()

    def __create_topics__(self):
        self.__cursor.execute(
            """
            CREATE TABLE if not exists Topics(
                id INTEGER PRIMARY KEY,
                author INTEGER,
                create_date DATE,
                create_time TIME,
                topic_name TEXT,
                topic_type INTEGER,
                FOREIGN KEY (author) REFERENCES Users (id),
                FOREIGN KEY (topic_type) REFERENCES TopicTypes (id)
            )
            """
        )

        self.__db.commit()

    def __create_messages__(self):
        self.__cursor.execute(
            """
            CREATE TABLE if not exists Messages(
                id INTEGER PRIMARY KEY,
                author INTEGER,
                create_date DATE,
                create_time TIME,
                topic INTEGER,
                message_text TEXT,
                FOREIGN KEY (author) REFERENCES Users (id),
                FOREIGN KEY (topic) REFERENCES Topics (id)
            )
            """
        )

        self.__db.commit()

    # API
    @property
    def cursor(self):
        return self.__cursor

    @property
    def db(self):
        return self.__db

    def fill_test_data(self):
        roles = [
            (1, 'admin'),
            (2, 'user')
        ]
        self.__cursor.executemany(
            """
            INSERT INTO UserRoles (id, name) VALUES (?, ?)
            """,
            roles
        )
        self.__db.commit()

        users = [
            (1, 1, 'admin', 'admin'),
            (2, 2, 'ivan', 'qwerty')
        ]
        self.__cursor.executemany(
            """
            INSERT INTO Users (id, role, user_name, password) VALUES (?, ?, ?, ?)
            """, 
            users
        )
        self.__db.commit()

        topic_types = [
            (None, 1, '2022-10-02', '12-30-00', 'news'),
            (None, 1, '2022-10-11', '06-11-12', 'python')
        ]
        self.__cursor.executemany(
            """
            INSERT INTO TopicTypes (id, author, create_date, create_time, name)
                VALUES (?, ?, ?, ?, ?)
            """, 
            topic_types
        )
        self.__db.commit()

        topic = [
            (None, 1, '2022-10-02', '12-30-00', 'topic 1', 2),
            (None, 1, '2022-10-11', '06-11-12', 'topic 2', 2),
            (None, 2, '2022-10-12', '09-00-00', 'topic 3', 1)
        ]
        self.__cursor.executemany(
            """
            INSERT INTO Topics (id, author, create_date, create_time, topic_name, topic_type)
                VALUES (?, ?, ?, ?, ?, ?)
            """, 
            topic
        )
        self.__db.commit()

        messages = [
            (None, 1, '2022-10-02', '12-30-00', 1, 'hahaha nice'),
            (None, 1, '2022-10-11', '06-11-12', 1, 'lol ssssss'),
            (None, 2, '2022-10-12', '09-00-00', 2, 'hmmmm, is not good!'),
            (None, 2, '2022-09-01', '17-30-00', 2, 'yep, it is so cute;)')
        ]
        self.__cursor.executemany(
            """
            INSERT INTO Messages (id, author, create_date, create_time, topic, message_text)
                VALUES (?, ?, ?, ?, ?, ?)
            """, 
            messages
        )
        self.__db.commit()

    def get_topic(self, id = None):
        query_string = """
            SELECT * FROM Topics
        """

        query_string += f"WHERE id = {id}" if id is not None else str()
        
        self.__cursor.execute(query_string)
        
        return self.__cursor.fetchall()

    def get_user_role(self, id = None):
        query_string = """
            SELECT * FROM UserRoles
        """

        query_string += f"WHERE id = {id}" if id is not None else str()
        
        self.__cursor.execute(query_string)
        
        return self.__cursor.fetchall()

    def get_user(self, id = None):
        query_string = """
            SELECT * FROM Users
        """

        query_string += f"WHERE id = {id}" if id is not None else str()
        
        self.__cursor.execute(query_string)
        
        return self.__cursor.fetchall()

    def get_topic_type(self, id = None):
        query_string = """
            SELECT * FROM TopicTypes
        """

        query_string += f"WHERE id = {id}" if id is not None else str()
        
        self.__cursor.execute(query_string)
        
        return self.__cursor.fetchall()

    def get_message(self, id = None):
        query_string = """
            SELECT * FROM Messages
        """

        query_string += f"WHERE id = {id}" if id is not None else str()
        
        self.__cursor.execute(query_string)
        
        return self.__cursor.fetchall()    

connector = Connector()
#connector.fill_test_data()

print(connector.get_topic())
print(connector.get_topic(1))
print()

print(connector.get_user_role())
print(connector.get_user_role(2))
print()

print(connector.get_user())
print(connector.get_user(2))
print()

print(connector.get_topic_type())
print(connector.get_topic_type(1))
print()

print(connector.get_message())
print(connector.get_message(4))
