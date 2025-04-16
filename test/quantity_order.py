from flask import Flask, request
import re
from twilio.twiml.messaging_response import MessagingResponse
from supabase import create_client, Client

app = Flask(__name__)

# Initialize Supabase client (replace with your credentials)
supabase: Client = create_client("YOUR_SUPABASE_URL", "YOUR_SUPABASE_KEY")

# Twilio messaging client setup would go here (simplified for example)
def send_message(to, body):
    response = MessagingResponse()
    response.message(body)
    return str(response)

# Parsing functions for different quantity types
def parse_full_half(message):
    message = message.lower()
    if "full" in message or "whole" in message:
        return "full"
    elif "half" in message:
        return "half"
    return None

def parse_number(message):
    digits = re.findall(r'\d+', message)
    if digits:
        return int(digits[0])
    number_words = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
    }
    for word, num in number_words.items():
        if word in message.lower():
            return num
    return None

def parse_volume(message):
    message_lower = message.lower()
    if "half liter" in message_lower:
        return 500  # 0.5 liter = 500ml
    numbers = re.findall(r'\d+(?:\.\d+)?', message)
    if not numbers:
        return None
    quantity = float(numbers[0])
    if "ml" in message_lower or "milliliter" in message_lower:
        return quantity
    elif "liter" in message_lower or "l" in message_lower:
        return quantity * 1000
    return quantity  # Assume ml if no unit specified

# Add item to order in Supabase
def add_to_order(user_id, item_code, quantity, quantity_type):
    supabase.table('orders').insert({
        'user_id': user_id,
        'item_code': item_code,
        'quantity_type': quantity_type,
        'quantity_value': str(quantity)  # Store as string for flexibility
    }).execute()

@app.route('/webhook', methods=['POST'])
def webhook():
    user_id = request.form['From']  # WhatsApp number
    message = request.form['Body'].strip()

    # Check user's current state
    user_state = supabase.table('user_states').select('*').eq('user_id', user_id).execute()

    if user_state.data and user_state.data[0]['state'] == 'waiting_for_quantity':
        current_item_code = user_state.data[0]['current_item_code']
        current_quantity_type = user_state.data[0]['current_quantity_type']
        item_name = supabase.table('items').select('item_name').eq('item_code', current_item_code).execute().data[0]['item_name']

        # Parse quantity based on type
        if current_quantity_type == 'full/half plate':
            quantity = parse_full_half(message)
            if quantity:
                add_to_order(user_id, current_item_code, quantity, current_quantity_type)
                supabase.table('user_states').update({'state': 'idle'}).eq('user_id', user_id).execute()
                return send_message(user_id, f"Added one {quantity} plate of {item_name} to your order. Add more items?")
            else:
                return send_message(user_id, "Please specify 'full' or 'half'.")

        elif current_quantity_type in ['one piece or more', 'number of plates']:
            quantity = parse_number(message)
            if quantity and quantity > 0:
                add_to_order(user_id, current_item_code, quantity, current_quantity_type)
                supabase.table('user_states').update({'state': 'idle'}).eq('user_id', user_id).execute()
                unit = "pieces" if current_quantity_type == 'one piece or more' else "plates"
                return send_message(user_id, f"Added {quantity} {unit} of {item_name} to your order. Add more items?")
            else:
                return send_message(user_id, "Please specify a positive number (e.g., '2' or 'two').")

        elif current_quantity_type == 'liter/ml':
            quantity = parse_volume(message)
            if quantity and quantity > 0:
                add_to_order(user_id, current_item_code, quantity, current_quantity_type)
                supabase.table('user_states').update({'state': 'idle'}).eq('user_id', user_id).execute()
                return send_message(user_id, f"Added {quantity} ml of {item_name} to your order. Add more items?")
            else:
                return send_message(user_id, "Please specify a valid quantity in ml or liters (e.g., '500ml' or '0.5 liter').")

    # No state or idle state: assume new order
    item = supabase.table('items').select('*').eq('item_code', message).execute()
    if item.data:
        item_code = item.data[0]['item_code']
        item_name = item.data[0]['item_name']
        quantity_type = item.data[0]['quantity_type']

        # Update or insert user state
        supabase.table('user_states').upsert({
            'user_id': user_id,
            'state': 'waiting_for_quantity',
            'current_item_code': item_code,
            'current_quantity_type': quantity_type
        }).execute()

        # Prompt for quantity based on type
        if quantity_type == 'full/half plate':
            return send_message(user_id, f"Would you like a full plate or a half plate of {item_name}?")
        elif quantity_type == 'one piece or more':
            return send_message(user_id, f"How many pieces of {item_name} would you like?")
        elif quantity_type == 'number of plates':
            return send_message(user_id, f"How many plates of {item_name} would you like?")
        elif quantity_type == 'liter/ml':
            return send_message(user_id, f"How many milliliters or liters of {item_name} would you like? (e.g., '500ml' or '0.5 liter')")
    else:
        return send_message(user_id, "Item code not found. Please enter a valid item code (e.g., '301' for paneer).")

if __name__ == '__main__':
    app.run(debug=True)