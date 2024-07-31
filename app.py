from flask import Flask, request, jsonify
import hmac
import hashlib
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Verify the webhook signature
        signature = request.headers.get('X-Hub-Signature-256')
        if not signature:
            return jsonify({'error': 'No signature header'}), 400

        secret = os.environ.get('WEBHOOK_SECRET', '').encode()
        body = request.data

        expected_signature = 'sha256=' + hmac.new(secret, body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected_signature):
            return jsonify({'error': 'Invalid signature'}), 400

        payload = request.json
        # Process the payload here
        print(payload)
        return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
