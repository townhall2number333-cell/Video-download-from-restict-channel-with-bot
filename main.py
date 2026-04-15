import telebot
import re
import time
import threading

# তোমার তথ্য
BOT_TOKEN = '7880805356:AAH5GLDkZbkZKkIQt0Mdd-rj_A1JqesmuEI'
LOG_CHANNEL_ID = -1003759758736 

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "রেলওয়ে সার্ভার থেকে বটটি সচল আছে। লিংক দিন।")

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    user_text = message.text
    link_pattern = r"https://t\.me/(?:c/)?([^/]+)/(\d+)"
    match = re.search(link_pattern, user_text)

    if match:
        channel_id_part = match.group(1)
        message_id = int(match.group(2))

        if channel_id_part.isdigit():
            source_chat_id = int(f"-100{channel_id_part}")
        else:
            source_chat_id = f"@{channel_id_part}"

        try:
            bot.send_message(LOG_CHANNEL_ID, f"User: @{message.from_user.username}\nLink: {user_text}")

            sent_msg = bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=source_chat_id,
                message_id=message_id
            )
            
            info_msg = bot.send_message(message.chat.id, "✅ ৬০ মিনিট পর এটি মুছে যাবে।")

            def auto_delete():
                time.sleep(3600)
                try:
                    bot.delete_message(message.chat.id, sent_msg.message_id)
                    bot.delete_message(message.chat.id, info_msg.message_id)
                except:
                    pass

            threading.Thread(target=auto_delete).start()

        except Exception as e:
            bot.reply_to(message, f"Error: {e}")

bot.infinity_polling()
            
