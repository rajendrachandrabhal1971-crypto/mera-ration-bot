
import os
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import telebot
from telebot import types

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable missing")

bot = telebot.TeleBot(BOT_TOKEN)

# Render Web Service health server
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

    def log_message(self, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = ThreadingHTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

UP_PORTAL = "https://nfsa.up.gov.in/"

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🙏 नमस्ते!\n"
        "Rajendra Ration PDF Bot में आपका स्वागत है।\n\n"
        "राशन कार्ड देखने के लिए भेजें:\n"
        "/ration 123456789012"
    )

@bot.message_handler(commands=["ration"])
def ration(message):
    parts = message.text.split()

    if len(parts) != 2 or not re.fullmatch(r"\d{12}", parts[1]):
        bot.reply_to(
            message,
            "❌ कृपया 12 अंकों का राशन कार्ड नंबर सही तरीके से भेजें।"
        )
        return

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "📄 सरकारी राशन कार्ड पोर्टल",
            url=UP_PORTAL
        )
    )

    bot.send_message(
        message.chat.id,
        "आपका नंबर दर्ज हो गया है।\n\n"
        "⚠️ सरकारी रिकॉर्ड की पुष्टि इस बॉट से अभी उपलब्ध नहीं है।\n"
        "अपना कार्ड देखने के लिए आधिकारिक पोर्टल खोलें।",
        reply_markup=markup
    )

print("Rajendra Ration PDF Bot started!")
bot.infinity_polling()
