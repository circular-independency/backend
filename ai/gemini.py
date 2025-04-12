from google import genai
import os
from db.db import Db
from ai.ai_utils import prepare_ai_category

class GeminiClient:

    KEY = os.getenv("GEMINI_API")

    @staticmethod
    def test():
        client = genai.Client(api_key=GeminiClient.KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", contents="Explain how AI works in a few words"
        )
        return response.text
    