import telebot, threading
from rag import ask

# BOT_TOKEN = '8616276906:AAH0SNc4yGhRfAgYKq_KjTnKTyBopdDG-Es'
BOT_TOKEN = '8981976763:AAELyBQalFKd__F_DNADsP6H78orM_-UmaI'

bot = telebot.TeleBot(BOT_TOKEN)

pending = {}

@bot.message_handler(func=lambda m: True)
def handle(message):
    user_id = message.chat.id
    ans, _ = ask(message.text)
    
    if ans == "ЭСКАЛАЦИЯ":
        pending[user_id] = message.text
        print(f"\n❓ {user_id}: {message.text}")
        bot.send_message(user_id, "🔄 Передаю специалисту.")
    else:
        bot.send_message(user_id, ans)

def console_reply():
    while True:
        text = input()
        if pending:
            uid, q = next(iter(pending.items()))
            bot.send_message(uid, f"👨‍💼 {text}")
            del pending[uid]

threading.Thread(target=console_reply, daemon=True).start()
bot.polling()