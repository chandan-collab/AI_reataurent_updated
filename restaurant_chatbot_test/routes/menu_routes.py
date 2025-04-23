from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from database.supabase_services import SupabaseService
from config import supabase
from datetime import datetime
import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from data.given_data import compress_image

menu_routes = Blueprint("menu_routes", __name__)
service = SupabaseService(supabase)
current_time = datetime.now().replace(microsecond=0).isoformat()

@menu_routes.route('/menu', methods=['GET'])
def menu():
    try:
        menu_items = service.get_menu_items()
    except Exception as e:
        menu_items = []
        print("Error fetching menu items:", e)
    return render_template('menu.html', menu_items=menu_items)

@menu_routes.route('/fetch_menu', methods=['GET'])
def fetch_menu():
    try:
        menu_items = service.get_menu_items()
    except Exception as e:
        menu_items = []
        print("Error fetching menu items:", e)
    return render_template('testmenu.html', menu_items=menu_items)

@menu_routes.route('/add_menu', methods=['POST'])
def add_menu():
    try:
        item = {
            "item_code": int(request.form['item_code']),
            "food_type": request.form['food_type'],
            "food_group": request.form['food_group'],
            "name": request.form['name'],
            "description": request.form['description'],
            "price": int(request.form['price']),
            "insert_time": current_time
        }
        supabase.table('menu').insert(item).execute()
        print("Menu item added!")
    except Exception as e:
        print("Add menu error:", e)
    return redirect(url_for('menu_routes.menu'))

@menu_routes.route('/edit_menu/<item_code>', methods=['GET', 'POST'])
def edit_menu(item_code):
    if request.method == 'GET':
        try:
            item = supabase.table('menu').select('*').eq('item_code', item_code).execute().data[0]
            return render_template('edit_menu.html', item=item)
        except Exception as e:
            print("Fetch error:", e)
            return redirect(url_for('admin_routes.admin_panel'))

    # POST
    try:
        supabase.table('menu').update({
            "name": request.form['name'],
            "description": request.form['description'],
            "price": int(request.form['price']),
            "updated_time": current_time
        }).eq('item_code', item_code).execute()
        print(f"Menu item {item_code} updated.")
    except Exception as e:
        print("Update error:", e)
    return redirect(url_for('menu_routes.menu'))

@menu_routes.route('/delete_menu/<item_code>', methods=['GET'])
def delete_menu(item_code):
    try:
        service.delete_menu_item(item_code)
        print(f"Deleted item {item_code}")
    except Exception as e:
        print("Delete error:", e)
    return redirect(url_for('menu_routes.menu'))

@menu_routes.route("/save_menu_screenshot", methods=["POST"])
def save_menu_screenshot():
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)
        driver.get("http://127.0.0.1:5000/fetch_menu")
        time.sleep(2)
        D = lambda x: driver.execute_script('return document.body.parentNode.scroll'+x)
        driver.set_window_size(D('Width'), D('Height'))
        driver.save_screenshot("static/menu_screenshot.png")
        compress_image("static/menu_screenshot.png", "static/menu_screenshot_compressed.jpg")
        os.remove("static/menu_screenshot.png")
        driver.quit()
        return jsonify({"message": "Screenshot saved!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
