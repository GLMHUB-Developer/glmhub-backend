from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import datetime
import base64

app = Flask(__name__)

# --- CONFIGURATION (Replace with your actual keys) ---
CONSUMER_KEY = "zXSRHAzExXCvGfyTGAKsyes83X5AE0xkVVhwcxI01f0AgnGb"
CONSUMER_SECRET = "ohtBP7AADYoo9IAE2CNSAEgo7VEFsvPdZDEzneGPwa9AXAs2Y7xrIRWzSRsGhPA5"
BUSINESS_SHORTCODE = "174379"  # Default Sandbox Shortcode
PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

@app.route('/')
def home():
    return "M-Pesa Backend is Live!"

@app.route('/stkpush', methods=['POST'])
def stk_push():
    data = request.get_json()
    phone = data.get('phone')  # e.g., 254712345678
    amount = data.get('amount')

    # 1. Get Access Token
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(api_url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    access_token = r.json().get('access_token')

    # 2. Generate Password
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = BUSINESS_SHORTCODE + PASSKEY + timestamp
    password = base64.b64encode(data_to_encode.encode()).decode('utf-8')

    # 3. Send STK Push
    checkout_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": "https://mydomain.com/path", # We will update this later
        "AccountReference": "GLM_HUB",
        "TransactionDesc": "Payment for services"
    }

    response = requests.post(checkout_url, json=payload, headers=headers)
    return jsonify(response.json())

import os

if __name__ == "__main__":
    # This line tells Flask to use the Port Render gives it
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)