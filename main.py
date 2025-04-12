from fastapi import FastAPI
from db.db import Db
from dotenv import load_dotenv
from api_types import WeekMealPlan
from db.models import FoodCategory, Shop, Item, ShoppingList
from lib import handle_meal_plan, scraped_to_items, get_user_shopping_list_for_bu, prepare_for_bu, bu_do_cart

import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

load_dotenv()
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/item/list")
def read_item_list():
    return Item.get_all()

@app.get("/shop/list")
def read_shop_list():
    return Shop.get_all()

@app.get("/shop/{shop_id}")
def read_shop(shop_id: int):
    return Shop.get_by_id(shop_id)

@app.get("/category/list")
def read_category_list():
    return FoodCategory.get_all()

@app.post("/plan/week")
async def handle_week_plan(week_plan: WeekMealPlan):
    mon = week_plan.monday
    tue = week_plan.tuesday
    wed = week_plan.wednesday
    thu = week_plan.thursday
    fri = week_plan.friday
    sat = week_plan.saturday
    sun = week_plan.sunday

    # here we will check if any ingredients were added aditionaly
    # TODO: handle that

    handle_meal_plan(mon)
    handle_meal_plan(tue)
    handle_meal_plan(wed)
    handle_meal_plan(thu)
    handle_meal_plan(fri)
    handle_meal_plan(sat)
    handle_meal_plan(sun)


    return {"status": 200}


@app.post("/category/add")
async def add_category(categories: list[FoodCategory]):
    for category in categories:
        category = FoodCategory(**category)
        FoodCategory.add(category)
    return {"status": 200}

@app.post("/item/add")
async def add_item(items: list[Item]):
    for item in items:
        item = Item(**item)
        Item.add(item)
    return {"status": 200}

@app.get("/parse/scrape")
async def parse_scraped_data():
    spar = "./scraped/spar_data.csv"
    scraped_to_items(spar, "spar")

    return {"status": 200}

@app.get("/shopping/list/{user_id}")
def get_shopping_list(user_id: int):
    qry = f"SELECT * FROM shopping_list WHERE user_id = {user_id} AND is_active = 1;"
    res = Db.select(qry)
    return res

@app.get("/shopping/items/{user_id}")
async def get_shopping_list(user_id: int):
    res = get_user_shopping_list_for_bu(user_id)
    bu_data = prepare_for_bu(res)

    await bu_do_cart(bu_data)

    return bu_data
