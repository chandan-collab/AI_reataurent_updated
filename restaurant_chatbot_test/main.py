from flask import Flask, request, jsonify, send_from_directory,render_template, request, jsonify, redirect, url_for
from datetime import datetime
from flask_cors import CORS
from core.chatbot import chatbot_response
from core.order_manager import place_order, confirm_order,get_all_orders
from core.menu import get_menu
from core.twilio_whatsapp import send_whatsapp_message
from twilio.twiml.messaging_response import MessagingResponse
from supabase import create_client, Client
from config import url, key
#for compressing image
import cv2, os , time
#for full screenshot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# # Initialize Flask App
app = Flask(__name__)
CORS(app)
supabase: Client = create_client(url, key)
new = datetime.now()
current_time=new.replace(microsecond=0).isoformat()

@app.route('/', methods=['GET', 'POST'])
def bot():
    """Handles incoming WhatsApp messages via Twilio."""
    if request.method == "GET":
        return "Webhook Verified!", 200

    incoming_msg = request.values.get("Body", "").strip().lower()
    user = request.values.get("From", "")
    response = MessagingResponse()
    msg = response.message()

    if "menu" in incoming_msg:
        msg.body(get_menu(user))   

    elif "order" in incoming_msg:
        order_details = incoming_msg.replace("order", "").strip()
        msg.body(place_order(user, order_details))

    elif "confirm" in incoming_msg:
        msg.body(confirm_order(user))

    else:
        msg.body(chatbot_response(incoming_msg))

    return str(response)


@app.route('/send', methods=['POST'])
def send_message():
    """Sends a message using Twilio WhatsApp API."""
    data = request.get_json()
    to_number = data.get('to')
    message_body = data.get('message')

    if not to_number or not message_body:
        return jsonify({'status': 'error', 'message': 'Missing "to" or "message" parameter.'}), 400
    
    return send_whatsapp_message(to_number, message_body)

#admin page
@app.route('/admin', methods=['GET'])
def admin_panel():
    """Display admin panel with menu items."""
    try:
        response = supabase.table('menu').select('*').execute()
        menu_items = response.data
    except Exception as e:
        menu_items = []
        print("Error fetching menu items:", e)

    return render_template('admin.html', menu_items=menu_items)

# delete a menu item
@app.route('/delete_menu/<item_code>', methods=['GET'])
def delete_menu(item_code):
    """Delete a menu item from Supabase."""
    try:
        supabase.table('menu').delete().eq('item_code', item_code).execute()
        print(f"Menu item {item_code} deleted successfully!")
    except Exception as e:
        print("Error deleting menu item:", e)

    return redirect(url_for('menu'))

# add a new menu item
@app.route('/add_menu', methods=['POST'])
def add_menu():
    """Insert a new menu item into Supabase."""

    item_code = int(request.form['item_code'])
    food_type = request.form['food_type']
    food_group = request.form['food_group']
    name = request.form['name']
    description = request.form['description']
    price = int(request.form['price'])

    try:
        supabase.table('menu').insert({
            "item_code": item_code,
            "food_type": food_type,
            "food_group": food_group,
            "name": name,
            "description": description,
            "price": price,
            "insert_time": current_time
        }).execute()
        print("Menu item added successfully!")
    except Exception as e:
        print("Error adding menu item:", e)

    return redirect(url_for('menu'))

# edit a menu item
@app.route('/edit_menu/<item_code>', methods=['GET', 'POST'])
def edit_menu(item_code):
    if request.method == 'GET':
        try:
            response = supabase.table('menu').select('*').eq('item_code', item_code).execute()
            item = response.data[0]
            return render_template('edit_menu.html', item=item)
        except Exception as e:
            print("Error fetching menu item:", e)
            return redirect(url_for('admin_panel'))

    # Handle POST request for updating menu items
    name = request.form['name']
    description = request.form['description']
    price = int(request.form['price'])

    try:
        supabase.table('menu').update({
            "name": name,
            "description": description,
            "price": price,
            "updated_time": current_time
        }).eq('item_code', item_code).execute()
        print(f"Menu item {item_code} updated successfully!")
    except Exception as e:
        print("Error updating menu item:", e)

    return redirect(url_for('menu'))


@app.route('/fetch_menu', methods=['GET'])
def fetch_menu():
    """Get the menu items."""
    try:
        # sql query---
        response = supabase.table('menu').select('*').execute()        
        menu_items = response.data if response.data else []       
        # print("list : ",menu_items)
    except Exception as e:
        menu_items = []
        print("Error fetching menu items:", e)

    return render_template('testmenu.html', menu_items=menu_items)

@app.route('/orders', methods=['GET'])
def orders():
    # """Display all orders."""
    # try:
    #     response = supabase.table('orders').select('*').execute()
    #     orders = response.data if response.data else []
    # except Exception as e:
    #     orders = []
    #     print("Error fetching orders:", e)

    return render_template('orders.html')#, orders=orders

@app.route("/save_menu_screenshot", methods=["POST"])
def save_menu_screenshot():
    try:
        options = Options()
        options.add_argument("--headless") #browser operates in the background without a GUI.
        options.add_argument("--disable-gpu")
        
        driver = webdriver.Chrome(options=options) #creates an instance of the Chrome browser, to control using Selenium.
        driver.get("http://127.0.0.1:5000/fetch_menu")  # Load the menu page
        
        time.sleep(2)  # wait for the page to load
        D= lambda x: driver.execute_script('return document.body.parentNode.scroll'+x)
        driver.set_window_size(D('Width'), D('Height'))  # Set the window size to the full page size
        driver.save_screenshot("static/menu_screenshot.png")  # Save the screenshot
        # driver.quit()
        # body = driver.find_element(By.CLASS_NAME, "menu-body")
        # body.screenshot("static/menu_screenshot.png")  # Save the screenshot of the body element

        compress_image("static/menu_screenshot.png", "static/menu_screenshot_compressed.jpg")

        screenshot_path = f"static/menu_screenshot.png"
        os.remove(screenshot_path)
        driver.quit()

        return jsonify({"message": "Full screenshot saved!", "screenshot_path": "static/menu_screenshot.png"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    """Display the menu page."""
    try:
        response = supabase.table('menu').select('*').execute()
        menu_items = response.data if response.data else []
    except Exception as e:
        menu_items = []
        print("Error fetching menu items:", e)

    return render_template('menu.html', menu_items=menu_items) 

@app.route("/get_today_orders")
def get_today_orders():
    """Fetch orders for today."""
    today =datetime.now().date().isoformat() # request.args.get("date")
    response = supabase.table("orders").select("*").eq("date", today).execute()
    return jsonify(response.data)

@app.route("/get_orders_by_date")
def get_orders_by_date():
    date = request.args.get("date")
    response = supabase.table("orders").select("*").eq("date", date).execute()
    return jsonify(response.data)

@app.route("/accept_order/<order_id>")
def accept_order(order_id):
    supabase.table("orders").update({"admin_action": "accepted"}).eq("id", order_id).execute()
    return jsonify({"message": "Order accepted"})

@app.route("/reject_order/<order_id>")
def reject_order(order_id):
    supabase.table("orders").update({"admin_action": "rejected"}).eq("id", order_id).execute()
    return jsonify({"message": "Order rejected"})

@app.route("/accept_all_orders")
def accept_all_orders():
    
    today = datetime.now().date().isoformat()
    print(f"Date : {today}")
    supabase.table("orders").update({"admin_action": "accepted"}).eq("date", today).execute()
    return jsonify({"message": "All orders accepted"})

def compress_image(image_path, output_path, quality=35): #100 is best quality, and 0 is lowest quality
    img = cv2.imread(image_path)
    cv2.imwrite(output_path, img, [cv2.IMWRITE_JPEG_QUALITY, quality])
#twilio has file size limits, and screenshots can be large.

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
