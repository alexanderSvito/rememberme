from math import exp
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class Pair:
    anchor: str
    response: str
    user_id: int
    correct: Decimal
    incorrect: Decimal
    correct_letters: Decimal
    incorrect_letters: Decimal

    @property
    def correct_rate(self):
        if self.incorrect == 0:
            return 1.0
        return self.correct * self.correct_letters / self.incorrect / len(self.response)

    @property
    def incorrect_rate(self):
        if self.incorrect == 0:
            return 1.0
        return self.incorrect_letters / self.incorrect / len(self.response)

    @property
    def score(self):
        return self.sigmoid(self.incorrect - self.correct)

    def sigmoid(self, x):
        return 1.0 / (1 + exp(-x))
