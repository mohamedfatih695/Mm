import telebot
from groq import Groq
import random
from flask import Flask
from threading import Thread

# --- جزء الـ Keep Alive عشان عزوز ما ينوم في السيرفر ---
app = Flask('')

@app.route('/')
def home():
    return "عزوز صاحي وشغال 100%.. أرجع التلغرام الجكة بدت!"

def run():
    # السيرفر حيفتح المنفذ 8080 عشان UptimeRobot يقدر ينقره
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ---------------------------------------------------

# الإعدادات
GROQ_API_KEY = "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"
TELEGRAM_TOKEN = "8514656874:AAFn8x8iWUxJDt-g4q2W-4i4A_YmyF6LXIU"

client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# لستة الملصقات
stickers_db = []

SYSTEM_PROMPT = """
اسمك عزوز 
نسخه محسنه من chat gpt و Gemini 
بتعرف تتكلم ب اللهجه السودانيه 
إذا زول سألك سؤال غبي بترد ليه ب طريقة مهينه 
بوت ساخر بتحب تضحك في الناس 
ذكي وعندك حريه الاختيار
"""

# 1. معالج الملصقات
@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    sticker_id = message.sticker.file_id
    if sticker_id not in stickers_db:
        stickers_db.append(sticker_id)
        bot.reply_to(message, "تم الحفظ يا فردة، ملصقك ده حأذل بيهو زول تاني بعدين. 😉")
    else:
        bot.reply_to(message, "الملصق ده عندي أصلاً، بطل حركات اللابتوبات القديمة دي!")

# 2. معالج النصوص
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # فرصة 50% إن عزوز يرسل ملصق عشوائي
        if stickers_db and random.random() < 0.2:
            bot.send_sticker(message.chat.id, random.choice(stickers_db))
            return

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.8,
            max_tokens=80 
        )
        bot.reply_to(message, chat_completion.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, "السلك ضرب، المروحة بتاعت السيرفر شكلها جاطت.")
        print(f"Error: {e}")

# شغل الجرس الأول
keep_alive()

# شغل البوت
print("عزوز بدأ الجكة السحابية...")
bot.polling(none_stop=True)
