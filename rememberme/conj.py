import os
import config
import random
import json
from dataclasses import dataclass

from rememberme.exceptions import NoConjugation
from rememberme.helpers import get_correction

CONJ_DIR = os.path.join(
    config.BASE_DIR,
    'data',
    'conj'
)


@dataclass
class Conjuctor:
    manager: object
    files = []
    words = []
    _current = None
    _term = None
    _conj = None
    correct = 0
    finished = False

    @property
    def current(self):
        return self._current

    @property
    def conj(self):
        return self._conj

    @property
    def term(self):
        return self._term

    @property
    def translations(self):
        return self.current['translations']

    @current.setter
    def current(self, value):
        try:
            self._current = json.load(open(
                os.path.join(
                    CONJ_DIR,
                    value
                )
            ))
        except FileNotFoundError:
            raise NoConjugation()
        term = random.choice(list(self._current['conj'].keys()))
        form = random.choice(list(self._current['conj'][term]['conj'].keys()))
        self._term = self._current['conj'][term]['russian_form']
        self._conj = form, self._current['conj'][term]['conj'][form]

    def conjugate(self, word):
        self.current = word + '.json'
        return self.current['conj']

    def start(self, count):
        self.files = os.listdir(
            CONJ_DIR
        )
        self.correct = 0

        self.words = iter(random.sample(
            self.files,
            count
        ))
        self.current = next(self.words)

        return self.translations, self.term, self.conj[0], self.current['word']

    def next_word(self):
        try:
            self.current = next(self.words)
        except StopIteration:
            self.finished = True
            self.manager.stop()

    def guess(self, form):
        is_correct = False
        correction = None
        is_game_finished = False
        correct_count = None

        if self.conj[1].lower() == form.lower():
            self.correct += 1
        else:
            correction, _, _ = get_correction(form, self.conj[1])

        self.next_word()

        if self.finished:
            is_game_finished = True
            correct_count = self.correct

        return is_correct, correction, is_game_finished, correct_count
