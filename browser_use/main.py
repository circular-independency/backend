import asyncio
import os

from playwright.sync_api import sync_playwright

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent, BrowserConfig
from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig

from typing import List
from pydantic import BaseModel

from browser_use import Agent, Controller

from task import *


async def run_search(task):
	load_dotenv()
	api_key = os.getenv('GEMINI_API_KEY')
	if not api_key:
		raise ValueError('GEMINI_API_KEY is not set')


	class Ingredient(BaseModel):
		name: str
		quantity: str
		price: float


	class ShoppingCart(BaseModel):
		posts: List[Ingredient]


	controller = Controller(output_model=ShoppingCart)

	llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

	browser = Browser(
		config=BrowserConfig(
			new_context_config=BrowserContextConfig(
				viewport_expansion=0,
				#allowed_domains=['mercatoronline.si', 'www.spar.si', 'hitrinakup.com']
			)
		)
	)
	async with await browser.new_context() as context:
		agent = Agent(
			task=task,
			llm=llm,
			max_actions_per_step=4,
			browser_context=context,
			#browser=browser,
			controller=controller,
		)

		history = await agent.run(max_steps=25)
		
		result = history.final_result()
		if result:
			parsed: ShoppingCart = ShoppingCart.model_validate_json(result)
			for post in parsed.posts:
				print('\n--------------------------------')
				print(f'Name:             {post.name}')
				print(f'Quantity:         {post.quantity}')
				print(f'Price:            {post.price}')
		else:
			print('No result')

		return result

def put_items_in_cart(store, shopping_list, preowned_ingridients):
	stores = {
		"mercator": {
			"link": "https://mercatoronline.si/"
		},
		"tus": {
			"link": "https://hitrinakup.com/priporoceni"
		},
		"spar": {
			"link": "https://www.spar.si/online/"
		}
	}
	load_dotenv()
	username = os.getenv('STORE_USERNAME')
	password = os.getenv('STORE_PASSWORD')

	task = generate_prompt(store, stores, username, password, shopping_list, preowned_ingridients, example)
	#print(task)

	asyncio.run(run_search(task))


if __name__ == '__main__':
	stores = {
		"mercator": {
			"link": "https://mercatoronline.si/"
		},
		"tus": {
			"link": "https://hitrinakup.com/priporoceni"
		},
		"spar": {
			"link": "https://www.spar.si/online/"
		}
	}
	# Example shopping list
	shopping_list = {
		"mercator": [
			{
				"name": "sladkor",
				"quantity": "1kg",
				"price": 1.5,
				"vendor_id": "726009",
				"source": "mercator"
			},
			{
				"name": "moka",
				"quantity": "1kg",
				"price": 2.0,
				"vendor_id": "21439",
				"source": "mercator"
			}
		],
		"spar": [
			{
				"name": "sladkor",
				"quantity": "1kg",
				"price": 1.5,
				"vendor_id": "439782",
				"source": "spar"
			},
			{
				"name": "moka",
				"quantity": "1kg",
				"price": 2.0,
				"vendor_id": "173873",
				"source": "spar"
			}
		],
		"tus": [
			{
				"name": "sladkor",
				"quantity": "1kg",
				"price": 1.5,
				"vendor_id": "439782",
				"source": "spar"
			},
			{
				"name": "moka",
				"quantity": "1kg",
				"price": 2.0,
				"vendor_id": "173873",
				"source": "spar"
			}
		]
	}

	preowned_ingridients = [
		{
			"name": "piščanec",
			"quantity": "1kg",
			"price": 2.0,
			"vendor_id": "12345",
			"source": "mercator"
		}
	]

	example = str([
			{
				"name": "sladkor",
				"quantity": "1kg",
				"price": 1.5
			},
			{
				"name": "moka",
				"quantity": "1kg",
				"price": 2.0
			}
	])

	store = "mercator"
	put_items_in_cart(store, shopping_list, preowned_ingridients)