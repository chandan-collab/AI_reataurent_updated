from config import url,key
from supabase import create_client, Client
from core.twilio_whatsapp import send_whatsapp_message
from data.given_data import MENU_IMAGE_URLS

supabase: Client = create_client(url, key)

def get_menu(user):           
    send_whatsapp_message(user, "Here is our menu:")
    for url in MENU_IMAGE_URLS:
        send_whatsapp_message(user, "", image_urls=[url])
    #     time.sleep(1) # time delay bcz twilio has limitation on send media 

# def menu_keys():  
#         response = supabase.table('menu').select('*').execute()
#         primary_keys = []
   
#         for item in response.data: # first time item ={item_code:301,name:paneer,discription:"deatils",price:50}
#             primary_keys.append(item['item_code']) # item['item_code] will append the values of item code
#         return primary_keys


def get_menu_dict():
    response = supabase.table('menu').select('item_code', 'name').execute()
    return {str(item['item_code']): item['name'] for item in response.data}
