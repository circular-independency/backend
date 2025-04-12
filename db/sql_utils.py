import sqlite3
import pandas as pd
from pydantic import BaseModel
from typing import Type

from db.db import Db


def initialize_db(sql_file_path: str, db_path: str):
    # Connect to SQLite DB (creates it if it doesn't exist)
    conn = sqlite3.connect(Db.DB_FILE)
    cursor = conn.cursor()

    # Read SQL schema
    with open(sql_file_path, 'r') as f:
        sql_script = f.read()

    # Execute SQL script
    cursor.executescript(sql_script)

    # Commit and close
    conn.commit()
    conn.close()
    print(f"Database initialized at: {db_path}")

def truncate_table(db_path: str, table_name:str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM {table_name};")
    conn.commit()
    conn.close()

def insert_dataframe_to_table(
    db_path: str,
    df: pd.DataFrame,
    model: Type[BaseModel],
    table_name: str
):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
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


def read_and_init_table(
    db_path: str,
    file_path: str,
    model: Type[BaseModel],
    table_name: str
):
    # Read CSV file into DataFrame
    df = pd.read_csv(file_path)
    truncate_table(db_path, table_name)
    insert_dataframe_to_table(db_path, df, model, table_name)



if __name__ == "__main__":
    # Set file paths
    sql_file = "20250412_dhdb_create_sqlite.sql"  # your SQL file
    db_file = "dhdb.sqlite"  # your output database file

    initialize_db(sql_file, db_file)
