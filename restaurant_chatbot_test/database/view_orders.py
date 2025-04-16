import os
from dotenv import load_dotenv
from supabase import create_client, Client
load_dotenv()


url: str = os.getenv("SUPA_URL")
key: str = os.getenv("SUPA_KEY")
supabase: Client = create_client(url, key)



response = supabase.table('orders').select('*', count="exact").execute() #use "orders"  to print orders detail
 
order = response.data   # list of dictionaries
order_text = "All orders are :\n"
if order:
    for row in order:
        # Convert the dictionary values to a list
        row_values = tuple(row.values())
        
        order_text += " : ".join(map(str, row_values)) + "\n"

   
print(order_text)




    
