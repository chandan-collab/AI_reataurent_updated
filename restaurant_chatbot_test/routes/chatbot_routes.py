from flask import Blueprint, request
from services.chatbot import chatbot_response
from services.twilio_whatsapp import send_whatsapp_message
from twilio.twiml.messaging_response import MessagingResponse
from flask import jsonify

chatbot_routes = Blueprint("chatbot_routes", __name__)

@chatbot_routes.route("/", methods=["GET", "POST"])
def bot():
    if request.method == "GET":
        return "Webhook Verified!", 200

    incoming_msg = request.values.get("Body", "").strip()
    user = request.values.get("From", "")
    response = MessagingResponse()
    response.message(chatbot_response(incoming_msg, user))
    return str(response)

@chatbot_routes.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    to_number = data.get('to')
    message_body = data.get('message')

    if not to_number or not message_body:
        return jsonify({'status': 'error', 'message': 'Missing "to" or "message" parameter.'}), 400

    return send_whatsapp_message(to_number, message_body)
