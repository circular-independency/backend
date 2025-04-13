import os
import sqlite3
import pandas as pd
from pydantic import BaseModel
from typing import Type

class Db:
    DB_NAME = "dhdb.sqlite"
    DB_FILE = os.path.join(os.path.dirname(__file__), DB_NAME)


    @staticmethod
    def select(qry):
        conn = sqlite3.connect(Db.DB_FILE)
        cursor = conn.cursor()

        cursor.execute(qry)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]

        conn.close()

        return result

    @staticmethod
    def insert(qry):
        conn = sqlite3.connect(Db.DB_FILE)
        cursor = conn.cursor()

        cursor.execute(qry)
        conn.commit()
        conn.close()

    @staticmethod
    def update(qry):
        conn = sqlite3.connect(Db.DB_FILE)
        cursor = conn.cursor()

        cursor.execute(qry)
        conn.commit()
        conn.close()


    @staticmethod
    def insert_dataframe_to_table(
        df: pd.DataFrame,
        model: Type[BaseModel],
        table_name: str
    ):
    # Connect to SQLite database
        conn = sqlite3.connect(Db.DB_FILE)
        cursor = conn.cursor()

        # Ensure all required fields in model are in the dataframe
        model_fields = [field for field in model.model_fields.keys() if field != 'id']
        missing_fields = [f for f in model_fields if f not in df.columns]
        if missing_fields:
            raise ValueError(f"Missing fields in DataFrame: {missing_fields}")

        # Prepare insert statement
        placeholders = ', '.join(['?'] * len(model_fields))
        columns = ', '.join(model_fields)
        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        

        # Prepare data rows from DataFrame using model validation
        records = []
        for _, row in df.iterrows():
            data = row[model_fields].to_dict()
            records.append(tuple(data.values()))

        # Execute inserts
        cursor.executemany(insert_sql, records)
        conn.commit()
        conn.close()
        print(f"Inserted {len(records)} records into table '{table_name}'.")


    
