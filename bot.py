import telebot
import config
from rememberme.manager import Manager

bot = telebot.TeleBot(config.TOKEN)
sessions = {}


def get_manager_or_default(message):
    if message.from_user.id in sessions:
        return sessions[message.from_user.id]
    else:
        manager = Manager(message.from_user.id)
        sessions[message.from_user.id] = manager
        return manager


def with_manager(func):
    def inner(message):
        manager = get_manager_or_default(message)
        return func(manager, message)
    return inner


def start_required(func):
    def inner(message, *args, **kwargs):
        manager = get_manager_or_default(message)
        if manager.is_play_mode():
            return func(message, *args, **kwargs)
        else:
            return manager.not_a_game_error()
    return inner


@bot.message_handler(commands=['start'])
@with_manager
def handle_start(manager, message):
    welcome = manager.start(message.text)
    bot.send_message(message.chat.id, welcome)


@bot.message_handler(commands=['help'])
@with_manager
def handle_help(manager, message):
    bot.send_message(message.chat.id, manager.get_help())


@bot.message_handler(commands=['guess'])
@with_manager
def handle_guess(manager, message):
    bot.send_message(message.chat.id, manager.get_guesser_start())
    word = manager.start_guesser(message.text)
    bot.send_message(
        270126879,
        f"{message.from_user.username} начал игру, слова:" +
        '\n'.join([w.anchor for w in list(manager.broker.words) + [manager.broker.current.anchor]])
    )
    bot.send_message(message.chat.id, word, parse_mode="Markdown")


@bot.message_handler(commands=['t', 'translate'])
@with_manager
def handle_translate(manager, message):
    word = manager.translate(message.text)
    bot.send_message(message.chat.id, word)


@bot.message_handler(commands=['play'])
@with_manager
def handle_play(manager, message):
    response = manager.start_game(message.text)
    bot.send_message(message.chat.id, response, parse_mode="Markdown")


@bot.message_handler(commands=['conj'])
@with_manager
def handle_conj(manager, message):
    response = manager.conj(message.text)
    bot.send_message(message.chat.id, response, parse_mode="Markdown")


@bot.message_handler(commands=['add'])
@with_manager
def handle_add(manager, message):
    response = manager.add_word(message.text)
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['edit'])
@with_manager
def handle_edit(manager, message):
    response = manager.edit_word(message.text)
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['del'])
@with_manager
def handle_del(manager, message):
    response = manager.del_word(message.text)
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['lang'])
@with_manager
def handle_lang(manager, message):
    response = manager.set_lang(message.text)
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['addpack'])
@with_manager
def handle_lang(manager, message):
    response = manager.add_pack(message.text)
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['listpacks'])
@with_manager
def handle_lang(manager, message):
    response = manager.list_packs(message.text)
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['stop'])
@start_required
@with_manager
def handle_stop(manager, message):
    bot.send_message(message.chat.id, manager.stop())


@bot.message_handler(content_types=["text"])
@with_manager
def repeat_all_messages(manager, message):
    result = manager.dispatch(message.text)
    bot.send_message(message.chat.id, result, parse_mode="Markdown")


if __name__ == '__main__':
    bot.polling(none_stop=True)

