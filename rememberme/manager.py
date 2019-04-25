from rememberme.guesser import Guesser
from data.sqlite import SQLighter
from rememberme.conj import Conjuctor
from rememberme.packs import PackManager
from rememberme.translator import Translator
from rememberme.parser import CommandParser
from rememberme.responser import Responser

parser = CommandParser()


class Manager:
    def __init__(self, user_id):
        self.db = SQLighter(user_id)
        self.mode = 'idle'
        self.broker = None
        self._lang = 'ru_ru'
        self.responser = Responser(self.lang)

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value):
        self._lang = value
        self.responser = Responser(self.lang)

    def is_play_mode(self):
        return self.mode != 'idle'

    def start(self):
        return self.responser.get_welcome_response()

    def set_lang(self, language):
        if 'ru' in language:
            self.lang = 'ru_ru'
            return self.responser.get_language_set_response()
        elif 'en' in language:
            self.lang = 'en_en'
            return self.responser.get_language_set_response()
        else:
            return self.responser.get_ambiguous_language_response()

    def get_help(self):
        return self.responser.get_help_response()

    def get_guesser_start(self):
        return self.responser.get_guesser_start_response()

    def not_a_game_error(self):
        return self.responser.get_not_a_game_response()

    @parser(r'^/(t|translate)\s(?P<word>.+)$')
    def translate(self, word):
        broker = Translator(self)
        translations = broker.translate(word)
        return self.responser.get_translate_response(translations)

    @parser(r'^/play\s(?P<count>\d+)$', count=5)
    def start_game(self, count: int):
        self.mode = 'conj'
        self.broker = Conjuctor(self)

        return self.responser.get_start_conj_response(
            *self.broker.start(count)
        )

    @parser(r'^/addpack\s(?P<pack_name>.+)$')
    def add_pack(self, pack_name: str):
        pack_manager = PackManager(self.db)

        return self.responser.get_add_pack_response(
            pack_manager.add_pack(pack_name)
        )

    @parser(r'^/listpacks$')
    def list_packs(self):
        pack_manager = PackManager(self.db)

        return self.responser.get_list_packs_response(
            pack_manager.get_packs()
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
            return self.responser.get_default_message()
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
        return self.responser.get_cancel_response()
