from config import url, key
from supabase import create_client
from datetime import datetime

# from core.order_manager import process_order_to_db
# connect to Supabase
supabase = create_client(url, key)

def process_order_to_db(user_phone, order_data):
    now = datetime.now()
    date = now.date().isoformat()
    time = now.strftime("%H:%M:%S")

    supabase.table("orders").insert({
        "order_id": order_data["order_id"],
        "user": user_phone,
        "order_details": order_data["order_details"],
        "food_quantity": order_data["food_quantity"],
        "parsed_json": order_data["parsed_json"],  
        "date": date,
        "time": time,
    }).execute()

# def confirm_order2(order_id, user):
#     print(f"Confirming order {order_id} ")
#     try:

#         # Step 1: Fetch order with matching id and user
#         result = supabase.table('orders').select("*").eq("order_id", order_id).eq("user", user).execute()
#         order_data = result.data

#         if not order_data:
#             return "No matching order found for this user."

#         # Step 2: Check if already confirmed or cancelled
#         current_status = order_data[0].get("status", "").lower()
#         if current_status == "confirmed":
#             return f"Your order {order_id} is already confirmed."
#         elif current_status == "cancelled":
#             return "This order was already cancelled."

#         # Step 3: Proceed with confirmation
#         update_response = supabase.table('orders').update({
#             "status": "confirmed"
#         }).eq("order_id", order_id).eq("user", user).execute()

#         if update_response.data:
#             return f"Your order *{order_id}* is confirmed !\nWe will prepare your fresh food shortly."
#         else:
#             return "Error confirming order. Please try again."

#     except Exception as e:
#         return f"Plese enter a order id."

def confirm_order(order_id, user):
    try:
        if not order_id:
            return "Please provide a valid order ID."
        # Fetch order using order_id and user
        result = supabase.table('orders').select("*").eq("order_id", order_id).eq("user", user).execute()
        order_data = result.data

        if not order_data:
            return f"⚠️ No matching order found for *{order_id}*."

        current_status = order_data[0].get("status", "").lower()
        if current_status == "confirmed":
            return f"Order *{order_id}* is already confirmed."
        elif current_status == "cancelled":
            return f"Order *{order_id}* has already been cancelled."

        # Update status
        update_response = supabase.table('orders').update({
            "status": "confirmed"
        }).eq("order_id", order_id).eq("user", user).execute()

        if update_response.data:
            return f"🎉 Your order *{order_id}* is now confirmed!\nWe'll prepare your food shortly."
        else:
            return "Failed to confirm the order. Please try again."

    except Exception as e:
        return f"❗ Something went wrong: {str(e)}"

def cancel_order(order_id, user):
    try:
        if not order_id:
            return "Please provide a valid order ID."
        # Step 1: Check for existing order with matching id and user
        result = supabase.table('orders').select("*").eq("order_id", order_id).eq("user", user).execute()
        order_data = result.data

        if not order_data:
            return "No matching order found for this user."

        # Step 2: Check current status
        current_status = order_data[0].get("status", "").lower()
        if current_status == "cancelled":
            return f"This order {order_id} is already cancelled."
        # elif current_status == "confirmed":
        #     return "Your order is already confirmed and can't be cancelled."

        # Step 3: Proceed with cancellation
        update_response = supabase.table('orders').update({
            "status": "cancelled"
        }).eq("order_id", order_id).eq("user", user).execute()

        if update_response.data:
            return f"Your order {order_id} has been cancelled successfully."
        else:
            return "Failed to cancel the order. Please try again."

    except Exception as e:
        return f"❗ Something went wrong: {str(e)}"
       
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