import os
import sqlite3

class Db:
    DB_NAME = "dhdb.sqlite"
    DB_FILE = os.path.join(os.path.dirname(__file__), DB_NAME)


    CONNECTION = None

    @staticmethod
    def connection():
        if Db.CONNECTION is None:
            Db.CONNECTION = sqlite3.connect(Db.DB_FILE)
        return Db.CONNECTION

    @staticmethod
    def disconnect(self):
        if Db.CONNECTION is not None:
            Db.CONNECTION.close()
            Db.CONNECTION = None


    
