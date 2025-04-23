from flask import Flask
from routes.admin_routes import admin_routes
from routes.menu_routes import menu_routes
from routes.order_routes import order_routes
from routes.chatbot_routes import chatbot_routes

app = Flask(__name__)

# Register route blueprints
app.register_blueprint(admin_routes)
app.register_blueprint(menu_routes)
app.register_blueprint(order_routes)
app.register_blueprint(chatbot_routes)

if __name__ == '__main__':
    app.run(debug=True)
