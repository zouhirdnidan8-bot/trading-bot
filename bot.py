import logging
from flask import Flask, request
import telebot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BOT_TOKEN = "8497280519:AAGiWs7C00K-sg62eCGEXkOVmKNmVrwJdc8"
CHAT_ID = "7165704391"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        if not data:
            return "No data received", 400
        
        symbol = data.get('symbol', 'UNKNOWN')
        signal_type = data.get('signal', 'SIGNAL')
        price = data.get('price', '0.00')
        poc = data.get('poc', '0.00')
        trend = data.get('trend', 'N/A')
        
        message = (
            f"🚨 **إشارة تداول جديدة من TradingView**\n"
            f"---------------------------------\n"
            f"💱 **الزوج:** `{symbol}`\n"
            f"📊 **الاتجاه / السيطرة:** {trend}\n"
            f"📍 **نقطة التحكم (POC):** `{poc}`\n"
            f"💰 **سعر الدخول:** `{price}`\n"
            f"🚀 **الإشارة:** **{signal_type}**\n"
            f"---------------------------------\n"
            f"⚠️ *تم الفحص عبر Volume Profile & SMC*"
        )
        
        bot.send_message(CHAT_ID, message)
        return "Success", 200
        
    except Exception as e:
        logging.error(f"Error handling webhook: {str(e)}")
        return "Error", 500

@app.route('/')
def home():
    return "Bot is running and ready for TradingView Webhooks!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
