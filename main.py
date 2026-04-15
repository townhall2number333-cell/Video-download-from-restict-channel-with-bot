import os
import subprocess
import sys
import re
import time
import threading

# ১. লাইব্রেরি অটোমেটিক চেক এবং ইন্সটল করার চেষ্টা
try:
    import telebot
except ImportError:
    print("Telebot library install kora hocche... please wait.")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI"])
    import telebot

# ২. তোমার দেওয়া তথ্যগুলো এখানে সেট করা হয়েছে
BOT_TOKEN = '7880805356:AAH5GLDkZbkZKkIQt0Mdd-rj_A1JqesmuEI'
LOG_CHANNEL_ID = -1003759758736 

bot = telebot.TeleBot(BOT_TOKEN)

print("--- Bot cholche... ---")

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "হ্যালো! আমাকে রেস্ট্রিক্টেড চ্যানেলের ভিডিও লিঙ্ক দিন। আমি সেটি দেব এবং ৬০ মিনিট পর ডিলিট করে দেব।")

# লিঙ্ক হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_link(message):
    user_text = message.text
    # টেলিগ্রাম লিঙ্ক শনাক্ত করার প্যাটার্ন
    link_pattern = r"https://t\.me/(?:c/)?([^/]+)/(\d+)"
    match = re.search(link_pattern, user_text)

    if match:
        channel_id_part = match.group(1)
        message_id = int(match.group(2))

        # সোর্স চ্যানেল আইডি নির্ধারণ
        if channel_id_part.isdigit():
            source_chat_id = int(f"-100{channel_id_part}")
        else:
            source_chat_id = f"@{channel_id_part}"

        try:
            # ক) লগ চ্যানেলে লিঙ্কটি সেভ করা
            user_info = f"User: @{message.from_user.username or message.from_user.id}\nLink: {user_text}"
            bot.send_message(LOG_CHANNEL_ID, user_info)

            # খ) ভিডিও বা কন্টেন্ট কপি করে পাঠানো
            sent_msg = bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=source_chat_id,
                message_id=message_id
            )
            
            info_msg = bot.send_message(message.chat.id, "✅ ভিডিও পাঠানো হয়েছে! এটি ৬০ মিনিট পর অটো-ডিলিট হয়ে যাবে।")

            # গ) অটো ডিলিট লজিক (Separate Thread)
            def auto_delete():
                time.sleep(3600)  # ৩৬০০ সেকেন্ড = ১ ঘণ্টা
                try:
                    bot.delete_message(message.chat.id, sent_msg.message_id)
                    bot.delete_message(message.chat.id, info_msg.message_id)
                except Exception as e:
                    print(f"Delete error: {e}")

            threading.Thread(target=auto_delete).start()

        except Exception as e:
            bot.reply_to(message, f"ভুল হয়েছে: {e}\n\nনিশ্চিত করুন বটটি ওই চ্যানেলে অ্যাডমিন হিসেবে আছে।")
    else:
        # লিঙ্ক না দিলে কোনো রেসপন্স করবে না অথবা চাইলে মেসেজ দিতে পারো
        pass

# বট চালু রাখা
bot.infinity_polling()
  
