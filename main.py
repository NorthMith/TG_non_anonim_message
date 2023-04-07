import telebot
from telebot import types
from config import TOKEN, ADMIN_CHAT_ID
import time

bot = telebot.TeleBot(TOKEN)

blocked_users = set()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Отправьте мне сообщение, и я передам его администратору.")

def get_username(user):
    return f"@{user.username}" if user.username else user.first_name

def get_user_profile_link(user):
    return f"tg://user?id={user.id}"

@bot.message_handler(func=lambda message: message.chat.id not in blocked_users)
def send_message_to_admin(message):
    username = get_username(message.from_user)
    bot.send_message(ADMIN_CHAT_ID, f"{username}: {message.text}", reply_markup=get_message_markup(message, username))
    bot.reply_to(message, "Спасибо! Ваше анонимное сообщение принято 👀")

def get_message_markup(message, username):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"Заблокировать {username}", callback_data=f"block_{message.chat.id}"))
    if not message.from_user.username:
        markup.add(types.InlineKeyboardButton(f"ID {message.chat.id}", url=get_user_profile_link(message.from_user)))
    markup.add(types.InlineKeyboardButton("Список заблокированных", callback_data="list_blocked"))
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith("block_"))
def block_user(call):
    user_id = int(call.data.split("_")[1])
    blocked_users.add(user_id)
    bot.answer_callback_query(call.id, f"Пользователь {user_id} заблокирован")

@bot.callback_query_handler(func=lambda call: call.data == "list_blocked")
def list_blocked_users(call):
    if not blocked_users:
        bot.answer_callback_query(call.id, "Список заблокированных пользователей пуст")
        return

    for user_id in blocked_users:
        user = bot.get_chat(user_id)
        username = get_username(user)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"Разблокировать {username}", callback_data=f"unblock_{user_id}"))
        bot.send_message(ADMIN_CHAT_ID, f"Заблокирован: {username}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("unblock_"))
def unblock_user(call):
    user_id = int(call.data.split("_")[1])
    blocked_users.discard(user_id)
    bot.answer_callback_query(call.id, f"Пользователь {user_id} разблокирован")

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(15)

