from typing import Union
from fastapi import FastAPI
from db.db import Db

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/shop/list")
def read_shop_list():
    conn = Db.connection()
    cursor = conn.cursor()

    qry = "SELECT * FROM shop;"
    cursor.execute(qry)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]

    return result


#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: Union[str, None] = None):
#    return {"item_id": item_id, "q": q}