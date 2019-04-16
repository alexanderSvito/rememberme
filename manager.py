import re
from dataclasses import dataclass

from guesser import Guesser
import config
from sqlite import SQLighter


@dataclass
class Manager:
    user_id: int
    mode: str = 'idle'
    broker: object = None

    def start_guesser(self):
        self.mode = 'guess'
        game = Guesser(self.user_id)
        self.broker = game
        return game.start()

    def add_word(self, message):
        command, anchor, response = re.split(r'\s', message)
        if command == '/add':
            db = SQLighter(config.words_db)
            db.insert_word_pair_for_user(self.user_id, anchor.lower(), response.lower())
            return anchor, response
        return False, False

    def dispatch(self, message):
        if self.mode == 'guess':
            return self.broker.guess(message)
