import os
import requests
import telebot
TELEGRAM_TOKEN = ""
OPENAI_API_KEY = ""

bot = telebot.TeleBot(TELEGRAM_TOKEN)

chat_history = {}

def generate_response(message_text, model, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": model,
        "prompt": message_text,
        "temperature": 0.8,
        "max_tokens": 150,
    }
    response = requests.post(
        "https://api.openai.com/v1/completions", headers=headers, json=data
    )
    response_json = response.json()
    message = response_json["choices"][0]["text"].strip()
    return message

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    message_text = message.text
    if chat_id not in chat_history:
        chat_history[chat_id] = {"history": "", "turn": 0}
    if message_text.lower() == "/start":
        chat_history[chat_id]["history"] = ""
        chat_history[chat_id]["turn"] = 0
        bot.send_message(
            chat_id, "Привет! Я готов к общению, задавай свои вопросы."
        )
    else:
        response = generate_response(message_text, "codex", OPENAI_API_KEY)
        chat_history[chat_id]["history"] += f"\nUser: {message_text}\nAI: {response}"
        bot.send_message(chat_id, response)

if __name__ == "__main__":
    bot.polling(none_stop=True)