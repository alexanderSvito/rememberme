import random
import difflib
from operator import attrgetter
from dataclasses import dataclass

from sqlite import SQLighter
import config


db = SQLighter(config.words_db)


@dataclass
class Guesser:
    user_id: int
    current = None
    words = []
    new_words = []

    def start(self):
        selected_words = self.get_words()
        if not selected_words:
            raise ValueError("There is no words in your dictinary now, please add one")

        random.shuffle(selected_words)
        self.words = iter(selected_words)
        self.current = next(self.words)

        return self.current.anchor

    def get_words(self, num=3):
        words = db.get_words_for_user(self.user_id)
        worst_words = sorted(words, key=attrgetter('score'))

        return self.select(worst_words, num)

    def select(self, objects, count=3):
        if not objects:
            return []

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
        self.next_word()

    def incorrect(self):
        self.current.incorrect += 1
        self.next_word()

    def next_word(self):
        try:
            self.new_words.append(self.current)
            self.current = next(self.words)
        except StopIteration:
            db.update_words(self.user_id, self.new_words)

    def guess(self, word):
        current_word = self.current

        if current_word.response.lower() == word.lower():
            self.correct()
            return "Correct:\n" + self.current.anchor
        else:
            diff = difflib.ndiff(word.lower(), current_word.response.lower())
            res = ''
            for letter in diff:
                if letter.startswith('-'):
                    res += letter[-1] + '\u0336'
                elif letter.startswith('+'):
                    res += letter[-1] + '\u0332'
                else:
                    res += letter[-1]

            self.incorrect()
            return res + '\n' + self.current.anchor
