from rememberme.guesser import Guesser
from data.sqlite import SQLighter
from rememberme.conj import Conjuctor
from rememberme.translator import Translator
from rememberme.parser import CommandParser
from rememberme.responser import Responser

parser = CommandParser()


class Manager:
    responser = Responser()

    def __init__(self, user_id):
        self.db = SQLighter(user_id)
        self.mode = 'idle'
        self.broker = None

    @parser(r'^/(t|translate)\s(?P<word>.+)$')
    def translate(self, word):
        broker = Translator(self)
        translations = broker.translate(word)
        return self.responser.get_translate_response(translations)

    @parser(r'^/play\s(?P<count>\d+)$', count=5)
    def start_game(self, count: int):
        self.mode = 'conj'
        self.broker = Conjuctor(self)
        trans, term, conj, word = self.broker.start(count)

        return self.responser.get_start_conj_response(
            term,
            trans,
            conj,
            word
        )

    @parser(r'^/conj\s(?P<word>.+)$')
    def conj(self, word):
        broker = Conjuctor(self)
        conj = broker.conjugate(word)
        return self.responser.get_conj_response(conj)

    @parser(r'^/guess\s(?P<count>\d+)$', count=10)
    def start_guesser(self, count: int):
        self.mode = 'guess'
        game = Guesser(self)
        self.broker = game
        word, stats = game.start(count)
        return self.responser.get_start_guess_response(word)

    @parser(r'^/add\s(?P<anchor>[\w_,()-]+)\s(?P<response>[\w_,()-]+)$')
    def add_word(self, anchor, response):
        if anchor.lower() == response.lower():
            return self.responser.get_same_word_response(anchor, response)
        try:
            anchor, response = self.db.insert_word_pair(anchor.lower(), response.lower())
        except:
            anchor, response = None, None
        return self.responser.get_created_response(anchor, response)

    @parser(r'^/edit\s(?P<anchor>[\w_,()-]+)\s(?P<response>[\w_,()-]+)$')
    def edit_word(self, anchor, response):
        if anchor.lower() == response.lower():
            return self.responser.get_same_word_response(anchor, response)
        try:
            count = self.db.edit_word_pair(anchor.lower(), response.lower())
        except:
            count = 0

        return self.responser.get_edited_response(count, anchor, response)

    @parser(r'^/del\s(?P<anchor>[\w_,()-]+)\s(?P<response>[\w_,()-]+)$')
    def del_word(self, anchor, response):
        try:
            count = self.db.del_word_pair(anchor.lower(), response.lower())
        except:
            count = 0

        return self.responser.get_deleted_response(count, anchor, response)

    def dispatch(self, message):
        if self.mode == 'idle':
            return 'Я вас не понял.'
        elif self.mode == 'guess':
            is_correct, is_finished, data = self.broker.guess(message)
            return self.responser.get_guess_response(
                is_correct, is_finished, **data
            )
        elif self.mode == 'conj':
            is_correct, is_finished, data = self.broker.guess(message)
            return self.responser.get_conj_game_response(
                is_correct, is_finished, **data
            )

    def stop(self):
        self.mode = 'idle'
        self.broker = object()
