from integrations.gemini_ai import get_gemini_response
from core.menu import get_menu,get_menu_dict
from core.order_manager import confirm_order, cancel_order,process_order_to_db
import re
from datetime import datetime

def chatbot_response(incoming_msg, user):
    """Central chatbot logic for WhatsApp messages."""
    incoming_msg = incoming_msg.lower().strip()

    if "hi" in incoming_msg or "hello" in incoming_msg or "hey" in incoming_msg:
        return "Hello! Welcome to Salad Restaurant.\nType for services:\n\n- menu\n- need help?"

    elif "menu" in incoming_msg:
        return get_menu(user)

    elif "order" in incoming_msg:
        order_details = incoming_msg.replace("order", "").strip()
        return handle_order_message(user, order_details)

    elif "confirm" in incoming_msg:
        order_id = incoming_msg.replace("confirm", "").strip()
        return confirm_order(order_id, user)

    elif "cancel" in incoming_msg:
        order_id= incoming_msg.replace("cancel", "").strip()
        return cancel_order(order_id,user)

    elif incoming_msg == "need help":
        return "For any query or order-related issue, please contact +911234567890."
    
    # Else, fallback to AI
    return get_gemini_response(incoming_msg)

def handle_order_message(user, message):
    # pattern = r"(\d+)\s*(full\s*plate|half\s*plate|full|half|plate|ml|l)?\s*(\d+)"
    # pattern = r"(\d+)\s*(full\s*plate|half\s*plate|full|half|plate|ml|litter|l)?\s*(\d{3})"
    pattern = r"(\d+)\s*(full\s*plates?|half\s*plates?|full|half|plates?|ml|liters?|l)?\s*(\d{3})"


    matches = re.findall(pattern, message.lower())

    if not matches:
        return "Invalid order format.\nTry something like: `2full 301, 500ml 406, 2 501`"

    menu_dict = get_menu_dict()  # Get {code: name}
    parsed_orders = []
    order_details = set()
    food_quantity_raw = []
    valid_items = []
    invalid_items = []
    order_id = 0

    for qty, unit, code in matches:
        unit = unit or "piece"
        parsed_orders.append({
            "code": code,
            "quantity": int(qty),
            "unit": unit
        })
        order_details.add(code)
        food_quantity_raw.append(f"{qty} {unit} {code}")

        if code in menu_dict:
            valid_items.append(code)
            order_id += int(code)
        else:
            invalid_items.append(code)
        print(f"valid : ")
    if invalid_items:
        return f"These item codes are invalid: {', '.join(invalid_items)}\nPlease check and try again."

    # Save order data to Supabase
    order_id += int(datetime.now().strftime("%M%S"))
    order_data = {
        "order_details": ",".join(order_details),
        "food_quantity": ", ".join(food_quantity_raw),
        "parsed_json": parsed_orders,
        "order_id": order_id
    }
    process_order_to_db(user, order_data)

    # Prepare preview
    order_preview = "\n".join([
        f"{o['quantity']} {o['unit']} - {menu_dict[o['code']]} (Code: {o['code']})"
        for o in parsed_orders
    ])
    

    return (
        f"📝 Your order is saved as *pending*:\n\n{order_preview}"
        f"\n*Order ID*: {order_id}"
        f"\n\nType *confirm* {order_id} to finalize or *cancel* {order_id} to discard."
    )
