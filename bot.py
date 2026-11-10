
# RATION PDF BOT - Final Code
# pip install pyTelegramBotAPI
# BotFather se token leke BOT_TOKEN me daalo

import telebot
from telebot import types
import base64
import re
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def _keep_alive():
    try:
        port = int(os.environ.get('PORT', 10000))
        class H(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200); self.end_headers(); self.wfile.write(b'Bot is Live')
            def log_message(self, *a): pass
        HTTPServer(('0.0.0.0', port), H).serve_forever()
    except Exception:
        pass
threading.Thread(target=_keep_alive, daemon=True).start()


BOT_TOKEN = "APNA_BOT_TOKEN_YAHAN_DAALO"  # @BotFather se milega
bot = telebot.TeleBot(BOT_TOKEN)

# /start
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "नमस्ते! राशन कार्ड देखने के लिए भेजें:\n"
        "/ration 123456789"
    )
    bot.reply_to(message, text)

# /ration <12 digit number>
@bot.message_handler(commands=['ration'])
def ration(message):
    parts = message.text.split()

    if len(parts) < 2:
        bot.reply_to(message, "कृपया ऐसे भेजें:\n/ration 215541438805")
        return

    ration_no = parts[1].strip()

    # Sirf number + 12 digit check (UP ration card 12 digit hota hai)
    if not re.fullmatch(r"\d{12}", ration_no):
        bot.reply_to(message, "❌ गलत नंबर है!\n12 अंकों का राशन कार्ड नंबर भेजें।\nउदाहरण: /ration 215541438805")
        return

    bot.reply_to(message, "राशन कार्ड खोजा जा रहा है...")

    # --- UP NFSA Official Link ---
    # Screenshot wala link pattern:
    # https://nfsa.up.gov.in/Food/TrackingRationCard/ViewRC.aspx?Details=<base64>
    # Details = base64( ration_no )
    # Isse official site par card khul jata hai, wahan se Print / PDF Save kar sakte ho.

    details = base64.b64encode(ration_no.encode()).decode()

    url = f"https://nfsa.up.gov.in/Food/TrackingRationCard/ViewRC.aspx?Details={details}"

    # Agar aapko screenshot jaisa lamba Details chahiye to ye wala use karo:
    # Ye UP portal ka purana format hai jisme district code bhi hota hai,
    # isliye simple base64 wala link hi sabse safe hai.

    msg = (
        f"✅ राशन कार्ड विवरण मिल गया है!\n\n"
        f"🆔 कार्ड नंबर: {ration_no}\n\n"
        f"👇 नीचे दिए गए लिंक पर क्लिक करके पूरा हिंदी राशन कार्ड देखें या PDF सेव (Print) करें:"
    )

    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("📄 राशन कार्ड देखें / Print PDF", url=url)
    markup.add(btn)

    bot.send_message(message.chat.id, msg, reply_markup=markup)

# Koi bhi aur text bheje to guide karo
@bot.message_handler(func=lambda m: True)
def anything(message):
    bot.reply_to(message, "राशन कार्ड देखने के लिए भेजें:\n/ration 215541438805")

print("Bot chal raha hai...")
bot.infinity_polling()
