import os
import config
import random
import json
from dataclasses import dataclass

from helpers import get_correction

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

    @current.setter
    def current(self, value):
        self._current = json.load(open(
            os.path.join(
                CONJ_DIR,
                value
            )
        ))
        term = random.choice(list(self._current['conj'].keys()))
        form = random.choice(list(self._current['conj'][term]['conj'].keys()))
        self._term = self._current['conj'][term]['russian_form']
        self._conj = form, self._current['conj'][term]['conj'][form]

    def translate(self, word):
        self.current = word + '.json'
        return self.current['translations']

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

        return (
            f"Начали, первое слово:\n"
            f"Форма - {self._term}\n"
            f"{self.conj[0]} ({self.current['word']})"
        )

    def next_word(self):
        try:
            self.current = next(self.words)
        except StopIteration:
            self.finished = True
            self.manager.stop()

    def guess(self, form):
        if self.conj[1].lower() == form.lower():
            result = 'Правильно!'
            self.correct += 1
        else:
            correction, _, _ = get_correction(form, self.conj[1])
            result = f'Неверно, правильный вариант:\n{correction}'

        self.next_word()

        if self.finished:
            result += f'\nИгра закончена, вы правильно назвали {self.correct} слов.'
        else:
            result += (
                f"\nСледующее слово:\n"
                f"Форма - {self._term}\n"
                f"{self.conj[0]} ({self.current['word']})"
            )
        return result
