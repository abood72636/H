# bot.py
import os
import time
import threading
from datetime import datetime
from flask import Flask
import telebot

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN missing in environment")

bot = telebot.TeleBot(TOKEN)
start_time = time.time()

def format_uptime(seconds):
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)

    parts = []
    if days > 0:
        parts.append(f"{days} يوم{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} ساعة")
    if minutes > 0:
        parts.append(f"{minutes} دقيقة")
    if not parts:
        parts.append("أقل من دقيقة")
    return " و".join(parts)

@bot.message_handler(commands=['start'])
def send_uptime(message):
    uptime_seconds = time.time() - start_time
    bot.reply_to(message, f"🤖 البوت يعمل منذ {format_uptime(uptime_seconds)}")

def run_telegram_polling():
    while True:
        try:
            # هذا سيبقي الـ polling يعمل مع إعادة تشغيل عند حدوث خطأ
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print("Polling error:", e)
            time.sleep(5)

# --- Flask health endpoint ---
app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

@app.route("/healthz")
def healthz():
    # رجّع 200 OK لكي تراه خدمات الـ ping على أنه جاهز
    return "OK", 200

if __name__ == "__main__":
    # شغّل البوت في ثريد مستقل
    t = threading.Thread(target=run_telegram_polling)
    t.daemon = True
    t.start()

    # Render يطلب أن نستمع على PORT من env
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
