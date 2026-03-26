
import requests
import telebot
import openai
import time

bot = telebot.TeleBot('bot_api')


client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="ai_api"
)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! я бот с опросами интересными стотьями "
                          "\n /fact команда с рандомным фактом"
                          "\n /article интересноя интернет статья о глобальном потеплении")


@bot.message_handler(commands=['fact'])
def global_warming_fact(message):
    bot.send_chat_action(message.chat.id, 'typing')

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system",
                 "content": "Ты — помощник, который даёт только короткие факты (2-3 предложения) о глобальном потеплении. Отвечай на языке пользователя."},
                {"role": "user",
                 "content": "Дай один короткий случайный факт о глобальном потеплении (не больше 3 предложений)."}
            ],
            temperature=0.7,
            timeout=20
        )
        fact = response.choices[0].message.content.strip()

        if '</think>' in fact:
            fact = fact.split('</think>')[-1].strip()

        bot.reply_to(message, f" *Факт о потеплении:*\n{fact}", parse_mode='Markdown')

    except Exception as e:
        print(f"Ошибка в /fact: {type(e).__name__} — {e}")
        bot.reply_to(message, "попробуйте позже.")

@bot.message_handler(commands=['article'])
def global_warming_fact(message):
    bot.send_chat_action(message.chat.id, 'typing')

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system",
                 "content": "ты памошник для поиска интересных статей о глобальном потеплении"},
                {"role": "user",
                 "content": "найди интересную статью про глобальное потепление"}
            ],
            temperature=0.7,
            timeout=20
        )
        fact = response.choices[0].message.content.strip()

        if '</think>' in fact:
            fact = fact.split('</think>')[-1].strip()

        bot.reply_to(message, f" *статья о потеплении:*\n{fact}", parse_mode='Markdown')

    except Exception as e:
        print(f"Ошибка в /fact: {type(e).__name__} — {e}")
        bot.reply_to(message, "попробуйте позже.")

bot.polling()
