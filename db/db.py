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
    def disconnect():
        if Db.CONNECTION is not None:
            Db.CONNECTION.close()
            Db.CONNECTION = None


    @staticmethod
    def select(qry):
        conn = Db.connection()
        cursor = conn.cursor()

        cursor.execute(qry)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]

        return result


    
