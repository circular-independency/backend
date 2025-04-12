from pydantic import BaseModel
from typing import Optional



class Ingredient(BaseModel):
    name: str
    amount: str


class Recipe(BaseModel):
    name: str
    ingredients: list[Ingredient]

class MealPlan(BaseModel):
    breakfast: Recipe
    lunch: Recipe
    dinner: Recipe

class WeekMealPlan(BaseModel):
    monday: MealPlan
    tuesday: MealPlan
    wednesday: MealPlan
    thursday: MealPlan
    friday: MealPlan
    saturday: MealPlan
    sunday: MealPlan

