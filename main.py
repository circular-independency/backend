from fastapi import FastAPI
from db.db import Db
from ai.gemini import GeminiClient
from dotenv import load_dotenv
from api_types import WeekMealPlan


load_dotenv()
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/shop/list")
def read_shop_list():
    qry = "SELECT * FROM shop;"
    result = Db.select(qry)
    return result

@app.get("/shop/{shop_id}")
def read_shop(shop_id: int):
    qry = f"SELECT * FROM shop WHERE id = {shop_id};"
    result = Db.select(qry)
    return result

@app.get("/category/list")
def read_category_list():
    qry = "SELECT * FROM food_category;"
    result = Db.select(qry)
    return result

@app.post("/plan/week")
def handle_week_plan(week_plan: WeekMealPlan):
    print(week_plan)
    return {"FUCK": "YOU"}

#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: Union[str, None] = None):
#    return {"item_id": item_id, "q": q}