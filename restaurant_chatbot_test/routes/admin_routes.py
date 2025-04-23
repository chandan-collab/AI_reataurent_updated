from flask import Blueprint, render_template
from database.supabase_services import SupabaseService
from config import supabase

admin_routes = Blueprint("admin_routes", __name__)
service = SupabaseService(supabase)

@admin_routes.route('/admin', methods=['GET'])
def admin_panel():
    try:
        menu_items = service.get_menu_items()
    except Exception as e:
        menu_items = []
        print("Error fetching menu items:", e)
    return render_template('admin.html', menu_items=menu_items)

@admin_routes.route('/orders', methods=['GET'])
def orders():
    return render_template('orders.html')
