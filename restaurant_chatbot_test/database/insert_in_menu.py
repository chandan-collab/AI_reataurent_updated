import os
from dotenv import load_dotenv
from supabase import create_client, Client
load_dotenv()


url: str = os.getenv("SUPA_URL")
key: str = os.getenv("SUPA_KEY")
supabase: Client = create_client(url, key)


menu_items = [
    {"item_code": 301, "name": "Paneer Tikka", "description": "Delicious paneer tikka", "price": 200},
    {"item_code": 305, "name": "Chicken Biryani", "description": "Spicy chicken biryani", "price": 350},
    {"item_code": 401, "name": "Roti", "description": "Soft wheat roti", "price": 20},
    {"item_code": 405, "name": "Butter Naan", "description": "Garlic butter naan", "price": 40},
    {"item_code": 501, "name": "Dal Makhani", "description": "Creamy dal makhani", "price": 180},
    {"item_code": 502, "name": "Tandoori Chicken", "description": "Smoky tandoori chicken", "price": 400},
    {"item_code": 601, "name": "Mango Lassi", "description": "Sweet mango lassi", "price": 80}
]

for item in menu_items:
    response = supabase.table("menu").insert(item).execute()
    print(f"Inserted: {response}")






##print menu
# response = supabase.table('menu').select('*', count="exact").execute() #use "orders"  to print orders detail
 
# menu_items = response.data   # list of dictionaries
# menu_text = "Our menu specializes in:\n"
# if menu_items:
#     for row in menu_items:
#         # Convert the dictionary values to a list
#         row_values = tuple(row.values())
        
#         menu_text += " : ".join(map(str, row_values)) + "\n"

   
# print(menu_text)