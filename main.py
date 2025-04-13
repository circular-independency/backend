import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.db import Db
from dotenv import load_dotenv
from api_types import WeekMealPlan
from db.models import FoodCategory, Shop, Item, Storage, ShoppingList
from lib import handle_meal_plan, scraped_to_items, get_user_shopping_list_for_bu, prepare_for_bu, bu_do_cart
from ai.gemini import GeminiClient
import json as json_module

load_dotenv()
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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

    shops = Shop.get_all()
    for shop in shops:
        shop = Shop(**shop)
        ShoppingList.shop_user_store_list(1, shop.id)


    week_plan_mapped = GeminiClient.map_ingredient_to_category(week_plan)
    week_plan_mapped = json_module.loads(week_plan_mapped)
    week_plan_mapped = WeekMealPlan(**week_plan_mapped)

    mon = week_plan_mapped.monday
    tue = week_plan_mapped.tuesday
    wed = week_plan_mapped.wednesday
    thu = week_plan_mapped.thursday
    fri = week_plan_mapped.friday
    sat = week_plan_mapped.saturday
    sun = week_plan_mapped.sunday
    
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
    qry = f"SELECT s.name as shop, fc.name_slo ,sum(i.grams) as grams_total FROM shopping_list as sl, item as i, shop as s, food_category as fc WHERE sl.user_id = {user_id} AND sl.is_active = 1 AND i.id = sl.item_id AND s.id = i.shop_id AND fc.id = i.food_category_id GROUP BY i.food_category_id;"
    res = Db.select(qry)
    return res

#@app.get("/shopping/items/{user_id}")
#async def get_shopping_list(user_id: int):
#    res = get_user_shopping_list_for_bu(user_id)
#    bu_data = prepare_for_bu(res)
#
#    await bu_do_cart(bu_data)
#
#    return bu_data


@app.get("/storage/list/{user_id}")
async def get_storage_list(user_id: int):
    qry = f"SELECT * FROM storage WHERE user_id = {user_id};"
    res = Db.select(qry)
    return res

@app.post("/shopping/shop/{shop_name}/{user_id}/{use_bu}")
async def shop_shopping_list(shop_name: str, user_id: int, use_bu: int):

    res = Shop.get_by_name(shop_name)[0]
    shop = Shop(**res)

    Storage.add_items_from_shop(user_id, shop.id)
    ShoppingList.shop_user_store_list(user_id, shop.id)

    if use_bu == 1:
        res = get_user_shopping_list_for_bu(user_id)
        bu_data = prepare_for_bu(res)

        await bu_do_cart(bu_data, shop_name)


    return {"status": 200}