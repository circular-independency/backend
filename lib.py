from db.models import Shop, Storage, Item, Recipe, ShoppingList
from api_types import MealPlan, Recipe
from ai.gemini import GeminiClient
import pandas as pd
import json as json_module
from db.db import Db
from bu.main import put_items_in_cart

def handle_meal_plan(meal_plan: MealPlan):
    breakfast = meal_plan.breakfast
    lunch = meal_plan.lunch
    dinner = meal_plan.dinner

    handle_recipe(breakfast)
    handle_recipe(lunch)
    handle_recipe(dinner)


def handle_recipe(recipe : Recipe):

    for ingredient in recipe.ingredients:   
        # check if we have ingredient in fridge
        # if it does not exist in category we will skip it and add it later
        # if we have it, check if we have enough of it
        check = Storage.user_has_category(ingredient.name, ingredient.amount)

        if not check:
            item = Item.get_cheapest_item_for_category(ingredient.name)

            if item is None:
                print(f"Item {ingredient.name} not found in database.")
                continue

            # add to user shopping list
            ShoppingList.add_item(item.id, 1)

    

#TODO: add async
def scraped_to_items(path: str, store_name : str) -> None:
    shop_res = Shop.get_by_name(store_name)[0]
    store = Shop(**shop_res)

    f = open(path, "r", encoding="utf-8")

    data = ""
    full_file = ""

    head = next(f)

    full_file += head

    while True:

        lines = [next(f, None) for _ in range(40)]
        lines = [line for line in lines if line is not None]
        if not lines:
            break

        chunk_no_head = head+''.join(lines)
        full_file += chunk_no_head

        chunk = head+chunk_no_head
        data += GeminiClient.scraped_parser(chunk, store.id)

    data = data.replace("][",",")

    f.close()
    #TODO: also add to the scraped cache?
    # use full_file for the scraped cache
    
    json = json_module.loads(data)
    df= pd.DataFrame(json).drop(columns=["id"])
    Db.insert_dataframe_to_table(df, Item, "item")


def get_user_shopping_list_for_bu(user:int):
    shops = Shop.get_all()
    out = {}

    for shop in shops:
        res = ShoppingList.get_user_shopping_list_for_shop_bu(user, shop["id"])
        out[shop["name"]] = res

    return out




def prepare_for_bu(data):
    out = {}
    for store in data:
        curr = data[store]
        
        store_data = []

        for item in curr:
            
            curr_item = {
				"name": item["name_slo"],
				"quantity": f"{item['grams']}g",
				"price": item["price"],
				"vendor_id": item["vendor_id"],
				"source": store
            }
            store_data.append(curr_item)

        out[store] = store_data

    return out

async def bu_do_cart(data, store):

    await put_items_in_cart(store, data, [])
