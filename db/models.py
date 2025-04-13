from pydantic import BaseModel
from typing import Optional
from datetime import date
import json as json_module

from db.db import Db


class Menu(BaseModel):
    id: int
    year: int
    week_number: int
    user_id: int
    mon_id: int
    tue_id: int
    wed_id: int
    thu_id: int
    fri_id: int
    sat_id: int
    sun_id: int


class Recipe(BaseModel):
    id: int
    name: str
    text: str


class RecipeItem(BaseModel):
    id: int
    recipe_id: int
    food_category_id: int
    grams: int

class Item(BaseModel):
    id: int
    price: float
    grams: int
    vendor_id: str
    src: Optional[str]
    food_category_id: int
    shop_id: int

    @staticmethod
    def add(item: "Item") -> None:
        qry = f"INSERT INTO item (price, grams, vendor_id, src, food_category_id, shop_id) VALUES ({item.price}, {item.grams}, '{item.vendor_id}', '{item.src}', {item.food_category_id}, {item.shop_id});"
        Db.insert(qry)

    @staticmethod
    def get_by_id(item_id: int) -> "Item":
        qry = f"SELECT * FROM item WHERE id = {item_id};"
        res = Db.select(qry)
        if len(res) == 0:
            raise ValueError(f"Item {item_id} not found in database.")
        return Item(**res[0])

    @staticmethod
    def get_default(category_id):
        test = {
            "id": 0,
            "price": 20.0,
            "grams": 100,
            "vendor_id": "",
            "src": None,
            "food_category_id": category_id,
            "shop_id": 1
        }
        return Item(**test)

    @staticmethod
    def get_cheapest_item_for_category(category: str) -> "Item":

        category_obj = FoodCategory.get_by_name(category)

        qry = f"SELECT * FROM food_category WHERE name = '{category}';"
        res = Db.select(qry)
        if len(res) == 0:
            raise ValueError(f"Category {category} not found in database.")
        
        category = FoodCategory(**res[0])
        qry = f"SELECT i.id, i.price, d.value, i.grams FROM item as i LEFT OUTER JOIN discount as d ON i.id = d.item_id WHERE i.food_category_id = {category.id};"
        res = Db.select(qry)
        if len(res) == 0:
            return Item.get_default(category_obj.id)
        

        best_price = 100000
        best_item = None
        for curr in res:
            if curr["value"] is not None:
                price = curr["price"] * (1 - curr["value"])
            else:
                price = curr["price"]

            if curr["grams"] <= 0:  
                curr["grams"] = 100

            price = price / curr["grams"]
            
            if price < best_price:
                best_price = price
                best_item = curr

        item = Item.get_by_id(best_item["id"])
        item.price = best_price

        return item

    @staticmethod
    def get_all() -> list["Item"]:
        qry = "SELECT * FROM item;"
        res = Db.select(qry)
        return res



class User(BaseModel):
    id: int
    name: str


class Storage(BaseModel):
    id: int
    grams: int
    expiry: Optional[date]
    user_id: int
    food_category_id: int


    @staticmethod
    def user_has_category(category_name: str, amount: int) -> bool:

        category = FoodCategory.get_by_name(category_name)

        if category is None:
            print(f"Category not found: {category_name}")
            return True

        user_id = 1
        result = Db.select(f"SELECT * FROM storage WHERE user_id = {user_id} AND food_category_id = {category.id} AND grams >= {amount};")

        return len(result) > 0

    @staticmethod
    def add_items_from_shop(user_id: int, shop_id: int) -> None:
        qry = f"SELECT * FROM shopping_list as sl, item as i WHERE sl.user_id = {user_id} AND sl.is_active = 1 AND i.shop_id = {shop_id} AND i.id = sl.item_id;"
        res = Db.select(qry)
        
        for curr in res:
            item = Item(**curr)
            qry = f"INSERT INTO storage (grams, user_id, food_category_id) VALUES ({item.grams}, {user_id}, {item.food_category_id});"
            Db.insert(qry)



class FoodCategory(BaseModel):
    id: int
    name: str
    name_slo: str
    kcal: int

    @staticmethod
    def add(category: "FoodCategory") -> None:
        qry = f"INSERT INTO food_category (name, kcal) VALUES ('{category.name}', {category.kcal});"
        Db.insert(qry)

    @staticmethod
    def get_by_name(name: str) -> "FoodCategory":
        qry = f"SELECT * FROM food_category WHERE name = '{name}';"
        res = Db.select(qry)
        if len(res) == 0:
            return None
        return FoodCategory(**res[0])
    
    @staticmethod
    def get_by_id(category_id: int) -> "FoodCategory":
        qry = f"SELECT * FROM food_category WHERE id = {category_id};"
        res = Db.select(qry)
        if len(res) == 0:
            return None
        return FoodCategory(**res[0])
    
    @staticmethod
    def get_all() -> list["FoodCategory"]:
        qry = "SELECT * FROM food_category;"
        res = Db.select(qry)
        return res

class Discount(BaseModel):
    id: int
    from_date: date
    to_date: date
    value: float
    item_id: Optional[int]


class Shop(BaseModel):
    id: int
    name: str
    site: Optional[str]

    @staticmethod
    def get_all() -> list["Shop"]:
        qry = "SELECT * FROM shop;"
        res = Db.select(qry)
        return res
    
    @staticmethod
    def get_by_id(shop_id: int) -> "Shop":
        qry = f"SELECT * FROM shop WHERE id = {shop_id};"
        res = Db.select(qry)
        return res
    
    @staticmethod
    def get_by_name(shop_name: str) -> "Shop":
        qry = f"SELECT * FROM shop WHERE name = '{shop_name}';"
        res = Db.select(qry)
        return res

class ShoppingList(BaseModel):
    id: int
    user_id: int
    item_id: int
    is_active: int


    @staticmethod
    def add_item(item_id: int, user_id: int) -> None:
        qry = f"INSERT INTO shopping_list (user_id, item_id, is_active) VALUES ({user_id}, {item_id}, {1});"
        Db.insert(qry)

    @staticmethod
    def get_user_shopping_list_for_shop_bu(user_id: int, shop_id:int):
        qry = f"SELECT i.vendor_id, fc.name_slo, s.name, s.site, i.grams, i.price FROM shopping_list as sl, item AS i , food_category as fc, shop as s WHERE user_id = {user_id} AND is_active = 1 AND sl.item_id = i.id AND fc.id = i.food_category_id AND i.shop_id = s.id AND s.id = {shop_id} ;"
        res = Db.select(qry)
        return res
    
    @staticmethod
    def shop_user_store_list(user_id: int, store_id:int):
        qry = f"UPDATE shopping_list SET is_active = 0 WHERE user_id = {user_id} AND item_id IN (SELECT id FROM item WHERE shop_id = {store_id});"
        Db.update(qry)

    

class Scraped(BaseModel):
    id: int
    shop_id: int
    store: str
    category: str
    mid_category: str
    product_id: str
    name: str
    price: str
    discount: str
    url: str