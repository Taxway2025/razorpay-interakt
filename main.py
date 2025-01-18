from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Webhook endpoint for Razorpay
@app.route('/webhook', methods=['POST'])
def razorpay_webhook():
    data = request.json  # Get Razorpay's payload
    print("Received data:", data)  # Debugging
    
    # Extract necessary information (like payment status, order ID)
    payment_status = data.get('payload', {}).get('payment', {}).get('entity', {}).get('status')
    contact = data.get('payload', {}).get('payment', {}).get('entity', {}).get('contact')

    if payment_status == "captured":
        # Call Interakt API to send a WhatsApp message
        send_message_to_interakt(contact)

    return jsonify({"status": "success"}), 200

# Function to call Interakt API
def send_message_to_interakt(phone_number):
    url = "https://api.interakt.ai/v1/public/message"  # Interakt API URL
    headers = {
        "Authorization": "Bearer YOUR_INTERAKT_API_KEY",  # Replace with your Interakt API key
        "Content-Type": "application/json"
    }
    payload = {
        "countryCode": "91",  # India country code
        "phoneNumber": phone_number,
        "type": "text",
        "message": "Your payment was successful! Thank you."
    }

    response = requests.post(url, json=payload, headers=headers)
    print("Interakt response:", response.json())

# Run the server
if __name__ == '__main__':
    app.run(port=5000)
