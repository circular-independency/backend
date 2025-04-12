from pydantic import BaseModel
from typing import Optional
from datetime import date


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
    discount_id: Optional[int]

class User(BaseModel):
    id: int
    name: str


class Storage(BaseModel):
    id: int
    grams: int
    expiry: Optional[date]
    user_id: int
    food_category_id: int


class FoodCategory(BaseModel):
    id: int
    name: str
    kcal: int

class Discount(BaseModel):
    id: int
    from_date: date
    to_date: date
    value: float


class Shop(BaseModel):
    id: int
    name: str
    site: str

