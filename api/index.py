import os
from flask import Flask, request
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")
SITE_URL = os.environ.get("SITE_URL")
if not TOKEN:
    raise Exception("Token Not Found")
if not SITE_URL:
    raise Exception("Site Url Not Found")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=SITE_URL + TOKEN)
    return "!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))