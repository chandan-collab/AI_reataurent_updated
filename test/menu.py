from supabase import create_client, Client
from restaurant_chatbot_test.config import url, key 

supabase = Client = create_client(url,key)
def menu_keys():  
        response = supabase.table('menu').select('*').execute()
        primary_keys = []
   
        for item in response.data: # first time item ={item_code:301,name:paneer,discription:"deatils",price:50}
            primary_keys.append(item['item_code']) # item['item_code] will append the values of item code
        return primary_keys


print("Menu Keys:", menu_keys()) # this will print the values of item code in the menu table