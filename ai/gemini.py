from google import genai
import os
from db.models import Item, FoodCategory
from api_types import WeekMealPlan

class GeminiClient:

    KEY = os.getenv("GEMINI_API_KEY")

    @staticmethod
    def test():
        client = genai.Client(api_key=GeminiClient.KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", contents="Explain how AI works in a few words"
        )
        return response.text
    
    @staticmethod
    def scraped_parser(inp:str, store_id:int) -> list[Item]:
        client = genai.Client(api_key=GeminiClient.KEY)
        
        categories = FoodCategory.get_all()

        promt = f"""
            {inp}
            This is a list of items scraped from a store.
            Please parse it and return a list of items in the provided JSON format.
            For store id use {store_id}.

            Map each item to the closest food category from the following list. DO NOT CREATE NEW CATEGORIES. Use the name column:
            {categories}

            Copy product_id column into vendor_id column.
        """

        response = client.models.generate_content_stream(
            model="gemini-2.0-flash-lite",
            contents=promt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': list[Item],
            },
        )

        out = ""

        for chunk in response:
            print(chunk.text, end="")
            out += chunk.text

        return out
    

    @staticmethod
    def map_ingredient_to_category(data):
        client = genai.Client(api_key=GeminiClient.KEY)
        
        categories = FoodCategory.get_all()

        promt = f"""
            {data}
            This is a list of items scraped from a store. Change all ingredient names to the closest food category from the following list. Use the name column:
            {categories}
            Please parse it and return a list of items in the provided JSON format.
        """

        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=promt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': WeekMealPlan,
            },
        )

        return response.text
    