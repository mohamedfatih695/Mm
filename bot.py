import telebot
from groq import Groq
import random

# الإعدادات
GROQ_API_KEY = "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"
TELEGRAM_TOKEN = "8514656874:AAFn8x8iWUxJDt-g4q2W-4i4A_YmyF6LXIU"

client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# لستة الملصقات (تذكر: في السحابة بتتمسح لو ما حطيتها هنا يدوياً بعد التجميع)
stickers_db = []

SYSTEM_PROMPT = """
اسمك عزوز 
نسخه محسنه من chat gpt و Gemini 
بتعرف تتكلم ب اللهجه السودانيه 
إذا زول سألك سؤال غبي بترد ليه ب طريقة مهينه 
بوت ساخر بتحب تضحك في الناس 
ذكي وعندك حريه الاختيار
"""

# 1. معالج الملصقات: يحفظ الملصق ويرد بأسلوب عزوز
@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    sticker_id = message.sticker.file_id
    if sticker_id not in stickers_db:
        stickers_db.append(sticker_id)
        bot.reply_to(message, "تم الحفظ يا فردة، ملصقك ده حأذل بيهو زول تاني بعدين. 😉")
    else:
        bot.reply_to(message, "الملصق ده عندي أصلاً، بطل حركات اللابتوبات القديمة دي!")

# 2. معالج النصوص: يربط مع Groq للرد الساخر
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # فرصة 20% إن عزوز يرسل ملصق عشوائي بدل الكلام
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
    except:
        bot.reply_to(message, "السلك ضرب، المروحة بتاعت السيرفر شكلها جاطت.")

bot.polling(none_stop=True)
