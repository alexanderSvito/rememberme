import telebot
import config
from rememberme.manager import Manager


bot = telebot.TeleBot(config.TOKEN)
sessions = {}


def start_required(func):
    def inner(message, *args, **kwargs):
        if message.from_user.id not in sessions:
            bot.send_message(message.chat.id, 'Используйте /start')
        else:
            return func(message, *args, **kwargs)
    return inner


@bot.message_handler(commands=['start'])
def handle_start(message):
    sessions[message.from_user.id] = Manager(message.from_user.id)
    bot.send_message(message.chat.id, "Привет, я помогу тебе запомнить что-то по принципу 'Якорь-Отклик' или сыграть с тобой в игру.")


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, """/start - начать сессию.
/help - помощь.
/add [якорь] [отклик] - добавить пару для запоминания. Если одно из слов содержит в себе пробелы, замените их на '_'. Например, 'hello_world'.
/play [количество=5] - начать игру по склонению слов.
/conj [слово] - просклонять польское слово.
/t(ranslate) [слово] - перевести польское слово на русский.
/stop - прервать текущую сессию.
/guess [количество=10] - начать игру по отгадыванию пар.""")


@bot.message_handler(commands=['guess'])
@start_required
def handle_guess(message):
    bot.send_message(message.chat.id, "Привет, сейчас мы вспомним пару слов")
    word = sessions[message.from_user.id].start_guesser(message.text)
    bot.send_message(message.chat.id, word, parse_mode="Markdown")


@bot.message_handler(commands=['t', 'translate'])
@start_required
def handle_translate(message):
    word = sessions[message.from_user.id].translate(message.text)
    bot.send_message(message.chat.id, word)


@bot.message_handler(commands=['play'])
@start_required
def handle_play(message):
    response = sessions[message.from_user.id].start_game(message.text)
    bot.send_message(message.chat.id, response, parse_mode="Markdown")


@bot.message_handler(commands=['conj'])
@start_required
def handle_translate(message):
    response = sessions[message.from_user.id].conj(message.text)
    bot.send_message(message.chat.id, response, parse_mode="Markdown")


@bot.message_handler(commands=['add'])
@start_required
def handle_add(message):
    response = sessions[message.from_user.id].add_word(message.text)
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['stop'])
@start_required
def handle_stop(message):
    sessions[message.from_user.id].stop()
    bot.send_message(message.chat.id, 'Отмена.')


@bot.message_handler(content_types=["text"])
@start_required
def repeat_all_messages(message):
    result = sessions[message.from_user.id].dispatch(message.text)
    bot.send_message(message.chat.id, result, parse_mode="Markdown")


if __name__ == '__main__':
    bot.polling(none_stop=True)

