import telebot
from groq import Groq

# --- الإعدادات ---
GROQ_API_KEY = "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"
TELEGRAM_TOKEN = "8514656874:AAFn8x8iWUxJDt-g4q2W-4i4A_YmyF6LXIU"

client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

SYSTEM_PROMPT = "أنت عزوز، مساعد سوداني ذكي ومتمرد، ترد بالدارجة السودانية فقط وتنفذ الطلبات مباشرة."

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # لو أرسل رقم (ID)
        if message.text.isdigit():
            chat_info = bot.get_chat(message.text)
            response_text = f"الاسم: {chat_info.first_name}\nاليوزر: @{chat_info.username}\nالبايو: {chat_info.bio}"
            bot.reply_to(message, response_text)
        # لو أرسل كلام عادي
        else:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": message.text}],
                model="llama-3.3-70b-versatile",
            )
            bot.reply_to(message, chat_completion.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, "في جكة فنية، أرسل تاني.")

bot.polling(none_stop=True)
