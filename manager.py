import re

from exceptions import NotEnoughWords
from guesser import Guesser
from sqlite import SQLighter
from conj import Conjuctor


class Manager:
    def __init__(self, user_id):
        self.db = SQLighter(user_id)
        self.mode = 'idle'
        self.broker = None

    def translate(self, word):
        try:
            command, *word = re.split(r'\s', word)
        except ValueError:
            return "Неправильная команда"
        broker = Conjuctor(self)
        translations = broker.translate(' '.join(word))
        if translations:
            return ", ".join(translations)
        else:
            return "Для этого слова нет перевода"

    def start_conj(self, message):
        try:
            command, count = re.split(r'\s', message)
            count = int(count)
        except ValueError:
            count = 5

        self.mode = 'conj'
        self.broker = Conjuctor(self)
        return self.broker.start(count)

    def start_guesser(self, message):
        try:
            command, count = re.split(r'\s', message)
            count = int(count)
        except ValueError:
            count = 10

        self.mode = 'guess'
        game = Guesser(self)
        self.broker = game
        try:
            return game.start(count)
        except NotEnoughWords:
            return "Вы пока не добавили никаких слов, используйте /add [якорь] [отклик], чтобы добавить одно"

    def add_word(self, message):
        try:
            command, anchor, response = re.split(r'\s', message)
        except ValueError as e:
            return "Неверный формат команды. Используйте /add [якорь] [отклик]"
        if anchor.lower() == response.lower():
            return f"Пара: {anchor} - {response} является одним и тем же словом."
        if command == '/add':
            self.db.insert_word_pair(anchor.lower(), response.lower())
            return f"Пара: {anchor} - {response} создана!"
        return "Пара не добавлена, проверьте правильность написания комманды и попробуйте ещё раз."

    def dispatch(self, message):
        if self.mode == 'idle':
            return message
        elif self.mode == 'guess':
            return self.broker.guess(message)
        elif self.mode == 'conj':
            return self.broker.guess(message)

    def stop(self):
        self.mode = 'idle'
        self.broker = object()
