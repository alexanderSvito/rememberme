import random
from operator import attrgetter
from dataclasses import dataclass

from exceptions import NotEnoughWords
from helpers import get_correction


@dataclass
class Guesser:
    manager: object

    current = None
    words = []
    new_words = []
    finished = False

    count = 0
    guessed = 0
    wrong_letters = 0

    def start(self, count=10):
        selected_words = self.get_words(count)

        if not selected_words:
            raise NotEnoughWords()

        random.shuffle(selected_words)
        self.words = iter(selected_words)
        self.current = next(self.words)

        return self.current.anchor.capitalize()

    def get_words(self, count):
        words = self.manager.db.get_words()
        worst_words = sorted(words, key=attrgetter('score'))

        return self.select(worst_words, count)

    def select(self, objects, count):
        if not objects:
            return []

        self.count = min(len(objects), count)

        if len(objects) < count:
            return objects

        results = []
        for i in range(count):
            pair = self.pick(objects)
            results.append(pair)
            objects.remove(pair)

        return results

    def pick(self, objects):
        total = sum([obj.score for obj in objects])
        for obj in objects:
            obj.probability = obj.score / total

        marker = random.random()
        anchor = 0

        for obj in objects:
            if marker < anchor + obj.score:
                return obj
            else:
                anchor += obj.score

        return objects[-1]

    def correct(self):
        self.current.correct += 1
        self.guessed += 1
        self.next_word()

    def incorrect(self, incorrect_letters, correct_letters):
        self.current.incorrect += 1
        self.current.incorrect_letters += incorrect_letters
        self.current.correct_letters += correct_letters
        self.wrong_letters += incorrect_letters
        self.next_word()

    def next_word(self):
        try:
            self.new_words.append(self.current)
            self.current = next(self.words)
        except StopIteration:
            self.finished = True
            self.finish()

    def finish(self):
        self.manager.db.update_words(self.new_words)

    def guess(self, word):
        current_word = self.current
        is_correct = False
        res = None

        if current_word.response.lower() == word.lower():
            self.correct()
            is_correct = True
        else:
            res, correct, incorrect = get_correction(word, current_word.response)
            self.incorrect(incorrect, correct)

        return is_correct, self.finished, res, self.current.anchor, self.count, int(self.wrong_letters / self.count)
