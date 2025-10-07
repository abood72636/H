import telebot
import os
import time
from datetime import datetime

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# وقت التشغيل
start_time = time.time()

def format_uptime(seconds):
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days} يوم{'' if days == 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} ساعة")
    if minutes > 0:
        parts.append(f"{minutes} دقيقة")
    
    if not parts:
        parts.append("أقل من دقيقة")
    
    return " و".join(parts)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    uptime_seconds = time.time() - start_time
    uptime_str = format_uptime(uptime_seconds)
    bot.reply_to(message, f"🤖 البوت يعمل منذ {uptime_str}")

bot.polling(non_stop=True)
