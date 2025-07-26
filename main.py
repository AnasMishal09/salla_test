<<<<<<< HEAD
from flask import Flask, jsonify
=======
from flask import Flask, request, jsonify
import requests
import hmac
import hashlib
>>>>>>> ec3f63fb98c70b2f9ebb0824a13b380070c26836
import os

app = Flask(__name__)

<<<<<<< HEAD

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
=======
# Read these from environment variables (will set later)
EXTERNAL_API_KEY = os.getenv("API9RQZ301753331276999")
EXTERNAL_API_URL = os.getenv("https://a-api.yokcash.com/api/order")
SALLA_WEBHOOK_SECRET = os.getenv("hello123")

def verify_signature(payload, signature):
    # Calculate HMAC SHA256 hash to verify webhook source
    computed = hmac.new(
        SALLA_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed, signature)

@app.route("/salla-webhook", methods=["POST"])
def salla_webhook():
    raw_body = request.get_data()
    signature = request.headers.get("X-Salla-Signature")

    if not verify_signature(raw_body, signature):
        return "Unauthorized", 401

    salla_data = request.json
    print("✅ Received from Salla:", salla_data)

    # Forward payload to external API
    headers = {
        "Authorization": f"Bearer {EXTERNAL_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(EXTERNAL_API_URL, json=salla_data, headers=headers)
    print("➡️ Sent to External API:", response.status_code, response.text)

    return jsonify({"status": "forwarded"}), 200

@app.route("/", methods=["GET"])
def home():
    return "✅ Webhook server is running!", 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
>>>>>>> ec3f63fb98c70b2f9ebb0824a13b380070c26836
