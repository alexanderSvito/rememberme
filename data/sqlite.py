from dataclasses import dataclass

import sqlite3


from rememberme.models import Pair
import config


@dataclass
class SQLighter:
    user_id: int

    @property
    def conncetion(self):
        return sqlite3.connect(config.words_db)

    def get_words(self):
        with self.conncetion as c:
            result = c.cursor().execute(f'SELECT * FROM words WHERE user_id = {self.user_id}').fetchall()
            return [Pair(*data) for data in result]

    def insert_word_pair(self, word_anchor, word_response):
        with self.conncetion as c:
            c.cursor().execute(
                f"""
                INSERT INTO words
                    (user_id, anchor, response, correct, incorrect, correct_letters, incorrect_letters)
                VALUES (?, ?, ?, 0, 0, 0, 0)
                """,
                (self.user_id, word_anchor, word_response)
            )

    def update_words(self, words):
        with self.conncetion as c:
            for word in words:
                c.cursor().execute(
                    f"""
                    UPDATE words
                        SET correct = ?, incorrect = ?, correct_letters =?, incorrect_letters = ?
                    WHERE user_id = ? AND anchor = ?
                    """,
                    (
                        word.correct,
                        word.incorrect,
                        word.correct_letters,
                        word.incorrect_letters,
                        self.user_id,
                        word.anchor
                    )
                )
