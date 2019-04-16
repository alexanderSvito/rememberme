import sqlite3

from models import Pair
import config


class SQLighter:

    def __init__(self, database):
        pass

    def __enter__(self):
        pass

    def __close__(self):
        self.close()

    def get_words_for_user(self, user_id):
        with sqlite3.connect(config.words_db) as connection:
            result = connection.cursor().execute(f'SELECT * FROM words WHERE user_id = {user_id}').fetchall()
            return [Pair(*data) for data in result]

    def insert_word_pair_for_user(self, user_id, word_anchor, word_response):
        with sqlite3.connect(config.words_db) as connection:
            connection.cursor().execute(
                f"""
                INSERT INTO words
                    (user_id, anchor, response, correct, incorrect)
                VALUES (?, ?, ?, 0, 0)
                """,
                (user_id, word_anchor, word_response)
            )

    def update_words(self, user_id, words):
        with sqlite3.connect(config.words_db) as connection:
            for word in words:
                connection.cursor().execute(
                    f"""
                    UPDATE words
                        SET correct = ?, incorrect = ?
                    WHERE user_id = ? AND anchor = ?
                    """,
                    (word.correct, word.incorrect, user_id, word.anchor)
                )

    def close(self):
        self.connection.close()
