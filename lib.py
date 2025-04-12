from db.models import Shop, Storage, Item, Recipe, ShoppingList
from api_types import MealPlan, Recipe
from ai.gemini import GeminiClient
import pandas as pd
import json as json_module
from db.db import Db

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
        # if we have it, check if we have enough of it
        check = Storage.user_has_category(ingredient.name, ingredient.amount)

        if not check:
            item = Item.get_cheapest_item_for_category(ingredient.name)
            # add to user shopping list
            ShoppingList.add_item(item.id, 1)

    

#TODO: add async
def scraped_to_items(path: str, store_name : str) -> None:
    shop_res = Shop.get_by_name(store_name)[0]
    store = Shop(**shop_res)

    f = open(path, "r")

    data = ""

    head = next(f)
    while True:

        lines = [next(f, None) for _ in range(40)]
        lines = [line for line in lines if line is not None]
        if not lines:
            break

        chunk = head+''.join(lines)
        data += GeminiClient.scraped_parser(chunk, store.id)

    data = data.replace("][",",")

    f.close()
    #TODO: also add to the scraped cache?
    
    json = json_module.loads(data)
    df= pd.DataFrame(json).drop(columns=["id"])
    Db.insert_dataframe_to_table(df, Item, "item")






