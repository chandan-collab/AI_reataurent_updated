from config import url, key
from core.menu import menu_keys, get_menu
from supabase import create_client
from datetime import datetime

# connect to Supabase
supabase = create_client(url, key)


def place_order(user, order_details):
    new = datetime.now()
    current_date = new.date().isoformat()
    current_time = new.time().replace(microsecond=0,second=0).isoformat()
    # current_time=new.replace(microsecond=0).isoformat()

    menu_items = menu_keys() # fetch primary keys
    
    order_items = order_details.replace(',', ' ').split() # split the order details into individual items (handles both comma & space separation)
    print(f"Order items: ",order_items)

    valid_items = []
    invalid_items = []

    # check the order items
    for item in order_items:
        if item in map(str, menu_items):
            valid_items.append(item)  #valid items
        else:
            invalid_items.append(item)  #invalid items

    print(f"Valid: {valid_items}, Invalid: {invalid_items}")
    
    
    if not valid_items:
        invalid_str= ", ".join(invalid_items)
        return f"{invalid_str} not present in our menu.\n\n{get_menu(user)}"

    # summary of valid items
    order_summary = ", ".join(valid_items)

    try:
        # store the order
        supabase.table('orders').insert({
            "user": user,
            "order_details": order_summary,
            "time": current_time,
            "date": current_date
        }).execute()

        # confirmation message
        response_text = f"Order received: {order_summary}\nType 'confirm' to proceed."

        # invalid items
        if invalid_items:
            response_text += f"\n\n(Note: We do not have {', '.join(invalid_items)} in our menu.)"

        return response_text

    except Exception as e:
        print(f"Error: {e}")
        return "Error saving order. Please try again."


def confirm_order(user):
    try:
        # update order status 
        response = supabase.table('orders').update({
            "status": "confirmed"
        }).eq("user", user).execute()

        # check if the order was updated
        if response.data:
            return "Your order is confirmed!\nWe will prepare your fresh food shortly."
        else:
            return "No order found for this user."

    except Exception as e:
        print(f"Error: {e}")
        return "Error confirming order. Please try again."

def get_all_orders():
    """Fetch all orders from Supabase."""
    try:
        response = supabase.table("orders").select("*").execute()

        if response.data:
            print("All orders:", response.data)
            return response.data
        else:
            print("No orders found.")
            return []
    except Exception as e:
        print("Error fetching all orders:", e)
        return []