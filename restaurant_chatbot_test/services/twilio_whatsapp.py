from twilio.rest import Client
import os

# Twilio credentials from environment variables or config
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(to_number, message_body, image_urls=None):
    """
    Sends a WhatsApp message using Twilio API.
    Supports multiple images.
    """
    try:
        message_params = {
            "from_": TWILIO_WHATSAPP_NUMBER,
            "body": message_body,
            "to": to_number
        }

        # Support multiple images
        if image_urls:
            if isinstance(image_urls, list):  # if multiple images 
                message_params["media_url"] = image_urls
            else:  # If single image
                message_params["media_url"] = [image_urls]

        message = client.messages.create(**message_params)  #** unpacking the dictionary into keyword arguments/ It allows you to dynamically pass a large number of arguments from a dictionary without manually listing each one.

        print(f"Message sent successfully. SID: {message.sid}")
        return {'status': 'success', 'sid': message.sid}

    except Exception as e:
        print(f"Failed to send message: {str(e)}")
        return {'status': 'error', 'message': str(e)}
