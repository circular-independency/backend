from dotenv import load_dotenv
import os

def shopping_list_to_string(shopping_list):
    """
    Convert the shopping list dictionary to a string format.
    """

    stringified = ""

    for item in shopping_list:
        stringified += f"- {item['name']} ({item['quantity']}) id: {item['vendor_id']}\n"

    return stringified

def preowned_ingridients_to_string(ingredients):
    """
    Convert the pre-owned ingredients list to a string format.
    """

    stringified = ""

    for item in ingredients:
        stringified += f"- {item['name']} ({item['quantity']})\n"

    return stringified

def generate_prompt_mercator(store, store_link, username, password, stringified_list, stringified_preowned, example):
    """
    Generate a prompt for the shopping agent for Mercator.
    """
    
    task = f"""
### Prompt for Shopping Agent - {store} Online Grocery Order

**Objective:**
Visit [{store}]({store_link}), search for the required grocery items, add them to the cart, select an appropriate delivery window, but do not complete the checkout process, stay on shopping cart page.

**Important:**
- Make sure that you don't buy more than it's needed for each article.
- After your search, if you click  the "V KOŠARICO" button, it adds the item to the basket.
- if you open the basket sidewindow menu, you can close it by clicking the "NADALJUJTE Z NAKUPOVANJEM" button on the top right. This will help you navigate easier.
- if there is a pop up window, you can close it by clicking the "X" button on the top right corner of the pop up window.
---

### Step 1: Navigate to the Website
- Open [{store}]({store_link}).
- You should log in as {username} by clicking on the button "Prijavite se". The password is : {password}

---

### Step 2: Add Items to the Basket
- Always firstly search for the item in the search bar by the ID parameter if it exists.
- If the item is not found, search for it by name, always in Slovenian language.

#### Shopping List:

{stringified_list}

At this stage, check the basket on the top right (indicates the price) and check if you bought the right items.

#### Ingredients I already have (DO NOT purchase):
{stringified_preowned}

---

### Step 3: Handling Unavailable Items
- If an item is **out of stock** (**Ni na zalogi**), find the best alternative.

---

### Step 4: Stay on the Cart Page
- proceed to the cart page ("Moja košarica") and check the items.
- if all the items are correct, proceed to the checkout page ("Nadaljujte z naslednjim korakom").
- if it's needed the username is: {username}
- and the password is : {password}
---

### Step 5: Select Delivery Window
- Select shipping to home ("Dostava na dom").
- Select the delivery address (address should be Večna pot 113, 1000 Ljubljana)
- Select the earliest available delivery window.
- If the delivery window is not available, select the next available one.
- Proceed with the checkout process ("Nadaljujte z naslednjim korakom") until the payment page, but do not complete the order.
- Stay on the checkout page (where it says "Izberite način plačila izdelkov")

### Step 5: Output Summary
- While on the checkout page, output a summary including:
- **Final list of items in cart** (including any substitutions).
Example:
{example}
- You must return the list of items in the same format as the example
- You must return the list of input items even if you are not sure that they are in the cart.
- You must return all the items that you got in the input.

**Important:** Ensure efficiency and accuracy throughout the process."""

    return task

def generate_prompt_spar(store, store_link, username, password, stringified_list, stringified_preowned, example):
    """
    Generate a prompt for the shopping agent for Spar.
    """
    
    task = f"""
### Prompt for Shopping Agent - {store} Online Grocery Order

**Objective:**
Visit [{store}]({store_link}), search for the required grocery items, add them to the cart, select an appropriate delivery window, proceed to checkout but do not buy the cart.

**Important:**
- Make sure that you don't buy more than it's needed for each article.
- After your search, if you click the "DODAJ V KOŠARICO" button or a button with the cart logo, it adds the item to the basket.
- Do not under any circumstances go to the Spar-mobile website.
---

### Step 1: Navigate to the Website
- Open [{store}]({store_link}).
- You should log in as {username} by clicking on the button with silhuette logo and then proceed to log in (PRIJAVA). The password is : {password}

---

### Step 2: Add Items to the Basket
- Always firstly search for the item in the search bar by the ID parameter if it exists.
- If the item is not found, search for it by name, always in Slovenian language.

#### Shopping List:

{stringified_list}

At this stage, check the basket on the top right (indicates the price) and check if you bought the right items.

#### Ingredients I already have (DO NOT purchase):
{stringified_preowned}

---

### Step 3: Handling Unavailable Items
- If an item is **out of stock** (**Ni na zalogi**), find the best alternative.

---

### Step 4: Stay on the Cart Page
- proceed to the cart page (logo of a cart) and check the items.
- if you didnt get for at least 25€ of items, get additional of the same item until you reach 25€.
- if all the items are correct, proceed to the checkout page ("Na blagajno").
- if it's needed the username is: {username}
- and the password is : {password}
---

### Step 5: Select Delivery Window
- Select drive in delivery ("Lokacije in ure prevzema").
- Select the delivery address (address should be Moskovska ulica 4, 1000 Ljubljana)
- Select the earliest available delivery window.
- If the delivery window is not available, select the next available one.
- Proceed with the checkout process ("Naprej") until the payment page, but do not complete the order.
- Stay on the checkout page (where it says "Izberite vrsto plačila")

### Step 5: Output Summary
- While on the checkout page, output a summary including:
- **Final list of items in cart** (including any substitutions).
Example:
{example}
- You must return the list of items in the same format as the example
- You must return the list of input items even if you are not sure that they are in the cart.
- You must return all the items that you got in the input.

**Important:** Ensure efficiency and accuracy throughout the process."""

    return task


def generate_prompt_tus(store, store_link, username, password, stringified_list, stringified_preowned, example):
    """
    Generate a prompt for the shopping agent for Tuš.
    """
    
    task = f"""
### Prompt for Shopping Agent - {store} Online Grocery Order

**Objective:**
Visit [{store}]({store_link}), search for the required grocery items, add them to the cart, select an appropriate delivery window, proceed to checkout but do not buy the cart.

**Important:**
- Make sure that you don't buy more than it's needed for each article.
- After your search, if you click the "DODAJ V KOŠARICO" button or a button with the cart logo, it adds the item to the basket.
---

### Step 1: Navigate to the Website
- Open [{store}]({store_link}).
- You should log in as {username} by clicking on the button with silhuette logo or button ("Prijava") and then proceed to log in (PRIJAVA). The password is : {password}

---

### Step 2: Add Items to the Basket
- Always firstly search for the item in the search bar by the ID parameter if it exists.
- If the item is not found, search for it by name, always in Slovenian language.

#### Shopping List:

{stringified_list}

At this stage, check the basket on the top right (indicates the price) and check if you bought the right items.

#### Ingredients I already have (DO NOT purchase):
{stringified_preowned}

---

### Step 3: Handling Unavailable Items
- If an item is **out of stock** (**Ni na zalogi**), find the best alternative.

---

### Step 4: Stay on the Cart Page
- proceed to the cart page (logo of a cart) and check the items.
- if you didnt get for at least 25€ of items, get additional of the same item until you reach 25€.
- if all the items are correct, proceed to the checkout page ("Zaključi nakup").
- if it's needed the username is: {username}
- and the password is : {password}
---

### Step 5: Select Delivery Window
- Select drive in delivery ("Lokacije in ure prevzema").
- Select the delivery address (address should be Pickup Tuš Vič, Cesta v Mestni log 84, Ljubljana)
- Select the earliest available delivery window.
- If the delivery window is not available, select the next available one.
- Proceed with the checkout process ("Naprej") until the payment page, but do not complete the order.
- Stay on the checkout page (where it says "Izberite vrsto plačila")

### Step 5: Output Summary
- While on the checkout page, output a summary including:
- **Final list of items in cart** (including any substitutions).
Example:
{example}
- You must return the list of items in the same format as the example
- You must return the list of input items even if you are not sure that they are in the cart.
- You must return all the items that you got in the input.

**Important:** Ensure efficiency and accuracy throughout the process."""

    return task

def generate_prompt(store, stores, username, password, shopping_list, preowned_ingredients, example):
    """
    Generate a prompt for the shopping agent based on the store and shopping list.
    """

    stringified_list = shopping_list_to_string(shopping_list[store])
    stringified_preowned = preowned_ingridients_to_string(preowned_ingredients)
    
    if store == "mercator":
        return generate_prompt_mercator(store, stores[store]["link"], username, password, stringified_list, stringified_preowned, example)
    elif store == "spar":
        return generate_prompt_spar(store, stores[store]["link"], username, password, stringified_list, stringified_preowned, example)
    elif store == "tus":
        return generate_prompt_spar(store, stores[store]["link"], username, password, stringified_list, stringified_preowned, example)