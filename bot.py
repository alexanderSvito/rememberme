import logging
import telebot
import config
from rememberme.manager import Manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(config.TOKEN)
sessions = {}


def get_manager_or_default(message):
    uid = message.from_user.id
    if uid not in sessions:
        sessions[uid] = Manager(uid)
    return sessions[uid]


def with_manager(func):
    def inner(message):
        manager = get_manager_or_default(message)
        return func(manager, message)
    return inner


@bot.message_handler(commands=['start'])
@with_manager
def handle_start(manager, message):
    bot.send_message(message.chat.id, manager.start())


@bot.message_handler(commands=['help'])
@with_manager
def handle_help(manager, message):
    bot.send_message(message.chat.id, manager.get_help())


@bot.message_handler(commands=['guess'])
@with_manager
def handle_guess(manager, message):
    bot.send_message(message.chat.id, manager.get_guesser_start())
    word = manager.start_guesser(message.text)
    bot.send_message(message.chat.id, word, parse_mode="Markdown")


@bot.message_handler(commands=['t', 'translate'])
@with_manager
def handle_translate(manager, message):
    word = manager.translate(message.text)
    bot.send_message(message.chat.id, word)


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
def handle_addpack(manager, message):
    response = manager.add_pack(message.text)
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['listpacks'])
@with_manager
def handle_listpacks(manager, message):
    response = manager.list_packs(message.text)
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['stop'])
@with_manager
def handle_stop(manager, message):
    if manager.is_play_mode():
        bot.send_message(message.chat.id, manager.stop())
    else:
        bot.send_message(message.chat.id, "No active session.")


@bot.message_handler(content_types=["text"])
@with_manager
def handle_text(manager, message):
    result = manager.dispatch(message.text)
    bot.send_message(message.chat.id, result, parse_mode="Markdown")


if __name__ == '__main__':
    logger.info("Bot starting...")
    bot.polling(none_stop=True)
