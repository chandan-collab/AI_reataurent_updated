# core/supabase_service.py

from supabase import Client

class SupabaseService:
    def __init__(self, client: Client):
        self.client = client

    # MENU OPERATIONS
    def get_menu_items(self):
        return self.client.table('menu').select('*').execute().data

    def get_menu_item_by_code(self, item_code):
        return self.client.table('menu').select('*').eq('item_code', item_code).execute().data

    def insert_menu_item(self, item_data):
        return self.client.table('menu').insert(item_data).execute()

    def update_menu_item(self, item_code, update_data):
        return self.client.table('menu').update(update_data).eq('item_code', item_code).execute()

    def delete_menu_item(self, item_code):
        return self.client.table('menu').delete().eq('item_code', item_code).execute()

    # ORDER OPERATIONS
    def get_orders(self):
        return self.client.table('orders').select('*').execute().data

    def get_orders_by_date(self, date):
        return self.client.table('orders').select('*').eq('date', date).execute().data

    def get_today_confirmed_orders(self, today):
        return self.client.table('orders').select('*').eq('date', today).eq('status', 'confirmed').execute().data

    def update_order_status(self, order_id, status):
        return self.client.table('orders').update({"status": status}).eq("order_id", order_id).execute()

    def update_admin_action(self, order_id, action):
        return self.client.table('orders').update({"admin_action": action}).eq("order_id", order_id).execute()

    def accept_all_today_orders(self, today):
        return self.client.table("orders").update({"admin_action": "accepted"}).eq("date", today).eq("status", "confirmed").execute()

    def get_order_by_id_user(self, order_id, user):
        return self.client.table('orders').select('*').eq("order_id", order_id).eq("user", user).execute().data
