import telebot
import random
import json
from telebot import types
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# 🔑 ВСТАВЬ СВОЙ ТОКЕН И ADMIN_ID
TOKEN = "8426470316:AAGbtkCd3P-UOx3GT9VkkrywAgPEAIgjJ-k"
ADMIN_ID = 123456789  # твой Telegram ID
bot = telebot.TeleBot(TOKEN)

# 📂 Файл для хранения данных
DATA_FILE = "dark_data.json"

# 🔧 Инициализация данных
try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
except:
    data = {"users": [], "quotes": [], "advices": [], "memes": []}

# 🔁 Функция для сохранения
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 🖤 Примерные тексты (если списки пустые)
if not data["quotes"]:
    data["quotes"] = [
        "🖤 Люди не меняются — они просто лучше прячут свои намерения.",
        "🧠 Кто контролирует эмоции — тот управляет ситуацией.",
        "💀 Молчание — сильнейшее оружие против манипуляции."
    ]
if not data["advices"]:
    data["advices"] = [
        "👁 Смотри на действия, а не на слова.",
        "🧩 Не раскрывай себя полностью — тайна даёт силу.",
        "🔥 Контролируй эмоции — и ты контролируешь людей."
    ]
if not data["memes"]:
    data["memes"] = [
        "😈 Мем: Когда манипулятор говорит, что он просто заботится о тебе 😏",
        "😂 Мем: 'Я не контролирую тебя' — говорит тот, кто проверяет твой онлайн 💀"
    ]

save_data()

# 🎛 Главное меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🧠 Цитата", "💀 Совет", "😈 Мем")
    markup.row("📊 Статистика")
    markup.row("🚫 Отписаться")
    return markup

# 🚀 Старт
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if user_id not in data["users"]:
        data["users"].append(user_id)
        save_data()
    bot.send_message(
        user_id,
        "🖤 Добро пожаловать в *Dark Mind — Тёмная психология*.\n\n"
        "Ты подписан на ежедневные цитаты и советы.\n\n"
        "Выбери, что хочешь получить 👇",
        reply_markup=main_menu(),
        parse_mode='Markdown'
    )

# 💬 Обработка сообщений
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.chat.id
    text = message.text

    if text == "🧠 Цитата":
        bot.send_message(user_id, random.choice(data["quotes"]))
    elif text == "💀 Совет":
        bot.send_message(user_id, random.choice(data["advices"]))
    elif text == "😈 Мем":
        bot.send_message(user_id, random.choice(data["memes"]))
    elif text == "📊 Статистика":
        bot.send_message(user_id, f"📈 Подписчиков: {len(data['users'])}")
    elif text == "🚫 Отписаться":
        if user_id in data["users"]:
            data["users"].remove(user_id)
            save_data()
            bot.send_message(user_id, "Ты отписался от рассылки 🖤")
        else:
            bot.send_message(user_id, "Ты не подписан.")
    elif user_id == ADMIN_ID and text.startswith("/add"):
        # /add quote Текст
        parts = text.split(" ", 2)
        if len(parts) < 3:
            bot.send_message(user_id, "❌ Формат: /add [quote|advice|meme] текст")
        else:
            category, value = parts[1], parts[2]
            if category in ["quote", "advice", "meme"]:
                key = {"quote": "quotes", "advice": "advices", "meme": "memes"}[category]
                data[key].append(value)
                save_data()
                bot.send_message(user_id, f"✅ Добавлено в {category}: {value}")
            else:
                bot.send_message(user_id, "❌ Категория должна быть quote/advice/meme")
    else:
        bot.send_message(user_id, "Выбери действие из меню 👇", reply_markup=main_menu())

# 🕒 Авторассылка каждый день в 09:00
def send_daily_post():
    text = random.choice(data["quotes"] + data["advices"])
    for user_id in data["users"]:
        try:
            bot.send_message(user_id, text)
        except:
            pass
    print(f"[{datetime.now().strftime('%H:%M')}] Ежедневная рассылка выполнена.")

scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_post, 'cron', hour=9, minute=0)
scheduler.start()

# 🚀 Запуск
print("Dark Mind Bot запущен...")
bot.infinity_polling()
