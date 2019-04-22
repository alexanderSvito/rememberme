import re

from rememberme.exceptions import NotEnoughWords, NoConjugation
from rememberme.guesser import Guesser
from data.sqlite import SQLighter
from rememberme.conj import Conjuctor
from rememberme.translator import Translator


class Manager:
    def __init__(self, user_id):
        self.db = SQLighter(user_id)
        self.mode = 'idle'
        self.broker = None

    def translate(self, word):
        try:
            command, *word = re.split(r'\s', word)
            word = ' '.join(word)
        except ValueError:
            return "Неправильная команда"

        broker = Translator(self)
        translations = broker.translate(word)

        if translations:
            return ", ".join(translations).capitalize()
        else:
            return "Для этого слова нет перевода"

    def start_game(self, message):
        try:
            command, count = re.split(r'\s', message)
            count = int(count)
        except ValueError:
            count = 5

        self.mode = 'conj'
        self.broker = Conjuctor(self)
        trans, term, conj, word = self.broker.start(count)

        return (
            f"Начали, первое слово:\n"
            f"Форма - _{term}_\n"
            f"Перевод - {', '.join(trans)}\n"
            f"> *{conj}* ({word})"
        )

    def conj(self, message):
        try:
            command, *words = re.split(r'\s', message)
            word = ' '.join(words)
        except ValueError:
            return "Неправильная команда"

        broker = Conjuctor(self)
        try:
            conj = broker.conjugate(word)
        except NoConjugation:
            return "Не могу просклонять этот глагол."

        res = ''
        for time, data in conj.items():
            res += f'*{data["russian_form"]}*\n'
            for pronoun, form in data['conj'].items():
                res += f'{pronoun}:  _{form}_\n'
            res += '\n'
        return res

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
            return "Начали! Первое слово:\n> " + game.start(count)
        except NotEnoughWords:
            return "Вы пока не добавили никаких слов, используйте /add [якорь] [отклик], чтобы добавить одно"

    def add_word(self, message):
        try:
            command, anchor, response = re.split(r'\s', message)
            anchor = " ".join(anchor.split("_"))
            response = " ".join(response.split("_"))
        except ValueError as e:
            return "Неверный формат команды. Используйте /add [якорь] [отклик]"
        if anchor.lower() == response.lower():
            return f"Пара: {anchor} - {response} является одним и тем же словом."
        if command == '/add':
            try:
                self.db.insert_word_pair(anchor.lower(), response.lower())
            except:
                return "Невозможно создать пару. Возможно, вы уже добавляли такое слово."
            return f"Пара: {anchor} - {response} создана!"
        return "Пара не добавлена, проверьте правильность написания комманды и попробуйте ещё раз."

    def get_response(self,
                     is_correct,
                     is_finished,
                     correct_word=None,
                     next_word=None,
                     correct_count=None,
                     average_count=None):
        response = ''
        if is_correct:
            response += "Правильно!"
        else:
            response += "Неверно:\n" + correct_word

        if is_finished:
            self.stop()
            response += (
                f"\nИгра окончена:\nУгадано {correct_count} "
                f"слов, среднее количество ошибок в слове: {average_count}"
            )
        else:
            response += '\nСледующее слово:\n> ' + next_word.capitalize()

        return response

    def dispatch(self, message):
        if self.mode == 'idle':
            return 'Я вас не понял.'
        elif self.mode == 'guess':
            return self.get_response(*self.broker.guess(message))
        elif self.mode == 'conj':
            is_correct, correction, is_game_finished, correct_count = self.broker.guess(message)
            if is_correct:
                result = 'Правильно!'
            else:
                result = f'Неверно, правильный вариант:\n{correction}'

            if is_game_finished:
                result += f'\nИгра закончена, вы правильно назвали {correct_count} слов.'
            else:
                result += (
                    f"\nСледующее слово:\n"
                    f"Форма - _{self.broker.term}_\n"
                    f"Перевод - {', '.join(self.broker.translations)}\n"
                    f"> *{self.broker.conj[0]}* ({self.broker.current['word']})"
                )
            return result

    def stop(self):
        self.mode = 'idle'
        self.broker = object()
