import telebot
import config
from manager import Manager
from collections import defaultdict

bot = telebot.TeleBot(config.TOKEN)
sessions = {}


def start_required(func):
    def inner(message, *args, **kwargs):
        if message.from_user.id not in sessions:
            bot.send_message(message.chat.id, 'Use /start')
        else:
            return func(message, *args, **kwargs)
    return inner


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    sessions[message.from_user.id] = Manager(message.from_user.id)
    bot.send_message(message.chat.id, "Привет, я помогу тебе запомнить что-то по принципу 'Якорь-Отклик'")


@bot.message_handler(commands=['guess'])
@start_required
def handle_start_help(message):
    bot.send_message(message.chat.id, "Привет, сейчас мы вспомним пару слов")
    word = sessions[message.from_user.id].start_guesser()
    bot.send_message(message.chat.id, word)


@bot.message_handler(commands=['add'])
@start_required
def handle_start_help(message):
    anchor, response = sessions[message.from_user.id].add_word(message.text)
    bot.send_message(message.chat.id, f"Пара: {anchor} - {response} создана!")


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    result = sessions[message.from_user.id].dispatch(message.text)
    bot.send_message(message.chat.id, result)


if __name__ == '__main__':
    bot.polling(none_stop=True)
