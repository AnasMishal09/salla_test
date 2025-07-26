from flask import Flask, request, jsonify  # Import Flask to handle web server and request parsing
import requests                             # Used to forward the webhook data to external API
import hmac                                 # For HMAC signature validation (used by Salla)
import hashlib                              # Used with HMAC for signature hashing
import os                                   # To read environment variables securely

# Create a Flask application instance
app = Flask(__name__)

# Read environment variables (defined in Railway later)
EXTERNAL_API_KEY = os.getenv("EXTERNAL_API_KEY")             # API key from the other store/platform
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL")             # External API endpoint (e.g., order creation)
SALLA_WEBHOOK_SECRET = os.getenv("SALLA_WEBHOOK_SECRET")     # Secret used to validate Salla webhook signature

# Function to verify Salla's webhook signature
def verify_signature(payload, signature):
    computed = hmac.new(
        SALLA_WEBHOOK_SECRET.encode(),   # Secret as bytes
        payload,                         # Raw request body
        hashlib.sha256                   # Hashing algorithm used by Salla
    ).hexdigest()
    return hmac.compare_digest(computed, signature)  # Prevent timing attacks

# Route to receive webhooks from Salla
@app.route("/salla-webhook", methods=["POST"])
def salla_webhook():
    raw_body = request.get_data()                      # Get raw body for signature check
    signature = request.headers.get("X-Salla-Signature")  # Signature sent by Salla

    # Validate the signature
    if not verify_signature(raw_body, signature):
        return "Unauthorized", 401

    # Parse the JSON payload
    salla_data = request.json
    print("✅ Received from Salla:", salla_data)

    # Prepare headers for external API request
    headers = {
        "Authorization": f"Bearer {EXTERNAL_API_KEY}",  # Use the external API key
        "Content-Type": "application/json"
    }

    # Forward the webhook data to the external API
    response = requests.post(EXTERNAL_API_URL, json=salla_data, headers=headers)
    print("➡️ Sent to External API:", response.status_code, response.text)

    # Respond to Salla that the webhook was processed
    return jsonify({"status": "forwarded"}), 200

# Optional health check route
@app.route("/", methods=["GET"])
def health():
    return "Webhook server is running!", 200

# Run locally (not used in Railway but useful for local testing)
if __name__ == "__main__":
    app.run(debug=True, port=5000)
    
