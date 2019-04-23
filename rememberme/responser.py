import random

import data.messages as msg
from data.answer_schemas import *


class Responser:
    messages = msg.__dict__

    def get_start_conj_response(self, term, translations, conj, round):
        scheme = self.fill_schema(CONJ_START_SCHEME)
        return scheme.format(
            term=term,
            translations=', '.join(translations),
            conj=conj,
            round=round
        )

    def get_translate_response(self, translations):
        if translations:
            return ', '.join(translations)
        else:
            raise ValueError(msg.TRANSLATION_ERROR_MSG)

    def get_conj_response(self, conj):
        if conj is None:
            return msg.NO_CONJUGATION_MSG

        res = ''
        for time, data in conj.items():
            res += f'*{data["russian_form"]}*\n'
            for pronoun, form in data['conj'].items():
                res += f'{pronoun}:  _{form}_\n'
            res += '\n'
        return res

    def get_start_guess_response(self, word):
        if word is None:
            return msg.NO_WORDS_MSG

        scheme = self.fill_schema(GUESSER_START_SCHEME)
        return scheme.format(
            round=word
        )

    def get_same_word_response(self, anchor, response):
        scheme = self.fill_schema(SAME_WORD_SCHEME)
        return scheme.format(
            anchor=anchor,
            response=response
        )

    def get_created_response(self, anchor, response):
        if anchor is None or response is None:
            return msg.DATABASE_ERROR_MSG

        scheme = self.fill_schema(CREATED_SCHEME)
        return scheme.format(
            anchor=anchor,
            response=response
        )

    def get_guess_response(self, is_correct, is_finished, **kwargs):
        if is_correct:
            scheme = CORRECT_SCHEME + '\n'
        else:
            scheme = WRONG_SCHEME + '\n'

        if is_finished:
            scheme += GAME_OVER_SCHEME
        else:
            kwargs['round'] = kwargs['round'].capitalize()
            scheme += NEXT_ROUND_SCHEME

        scheme = self.fill_schema(scheme)

        return scheme.format(**kwargs)

    def get_conj_game_response(self,
                               is_correct,
                               is_finished,
                               **kwargs):
        if is_correct:
            scheme = CORRECT_SCHEME + '\n'
        else:
            scheme = WRONG_SCHEME + '\n'

        if is_finished:
            scheme += GAME_OVER_SCHEME
        else:
            kwargs['round'] = kwargs['round'].capitalize()
            scheme += NEXT_CONJ_ROUND_SCHEME

        scheme = self.fill_schema(scheme)

        return scheme.format(**kwargs)

    def get_edited_response(self, count, anchor, response):
        if anchor is None or response is None:
            return msg.DATABASE_ERROR_MSG

        if count == 0:
            return msg.NOT_FOUND

        scheme = self.fill_schema(EDITED_SCHEME)
        return scheme.format(
            anchor=anchor,
            response=response
        )

    def get_deleted_response(self, count, anchor, response):
        if anchor is None or response is None:
            return msg.DATABASE_ERROR_MSG

        if count == 0:
            return msg.NOT_FOUND

        scheme = self.fill_schema(DELETED_SCHEME)
        return scheme.format(
            anchor=anchor,
            response=response
        )

    def fill_schema(self, scheme, **kwargs):
        messages = {
            identifier: random.choice(options)
            if isinstance(options, list) else options
            for identifier, options
            in self.messages.items()
        }

        static_scheme = scheme.format(**messages)

        return static_scheme
