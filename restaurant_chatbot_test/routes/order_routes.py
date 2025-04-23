from flask import Blueprint, request, jsonify
from datetime import datetime
from config import supabase

order_routes = Blueprint("order_routes", __name__)

@order_routes.route("/get_today_orders")
def get_today_orders():
    today = datetime.now().date().isoformat()
    response = supabase.table("orders").select("*").eq("date", today).eq("status", "confirmed").execute()
    return jsonify(response.data)

@order_routes.route("/get_orders_by_date")
def get_orders_by_date():
    date = request.args.get("date")
    response = supabase.table("orders").select("*").eq("date", date).execute()
    return jsonify(response.data)

@order_routes.route("/accept_order/<order_id>")
def accept_order(order_id):
    supabase.table("orders").update({"admin_action": "accepted"}).eq("order_id", order_id).execute()
    return jsonify({"message": "Order accepted"})

@order_routes.route("/reject_order/<order_id>")
def reject_order(order_id):
    supabase.table("orders").update({"admin_action": "rejected"}).eq("order_id", order_id).execute()
    return jsonify({"message": "Order rejected"})

@order_routes.route("/accept_all_orders")
def accept_all_orders():
    today = datetime.now().date().isoformat()
    supabase.table("orders").update({"admin_action": "accepted"}).eq("date", today).eq("status", "confirmed").execute()
    return jsonify({"message": "All orders accepted"})
