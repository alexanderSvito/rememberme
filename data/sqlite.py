import sqlite3
from dataclasses import dataclass

from rememberme.models import Pair
import config


@dataclass
class SQLighter:
    user_id: int

    @property
    def connection(self):
        return sqlite3.connect(config.words_db)

    def ensure_table(self):
        with self.connection as c:
            c.execute('''
                CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    anchor TEXT,
                    response TEXT,
                    correct INTEGER DEFAULT 0,
                    incorrect INTEGER DEFAULT 0,
                    correct_letters INTEGER DEFAULT 0,
                    incorrect_letters INTEGER DEFAULT 0,
                    UNIQUE(user_id, anchor)
                )
            ''')

    def get_words(self):
        with self.connection as c:
            result = c.execute(
                'SELECT anchor, response, user_id, correct, incorrect, '
                'correct_letters, incorrect_letters '
                'FROM words WHERE user_id = ?',
                (self.user_id,)
            ).fetchall()
            return [Pair(*data) for data in result]

    def insert_word_pair(self, word_anchor, word_response):
        with self.connection as c:
            c.execute(
                'INSERT INTO words '
                '(user_id, anchor, response, correct, incorrect, '
                'correct_letters, incorrect_letters) '
                'VALUES (?, ?, ?, 0, 0, 0, 0)',
                (self.user_id, word_anchor, word_response)
            )
        return word_anchor, word_response

    def edit_word_pair(self, word_anchor, word_response):
        with self.connection as c:
            cursor = c.execute(
                'UPDATE words SET response = ?, correct = 0, incorrect = 0, '
                'correct_letters = 0, incorrect_letters = 0 '
                'WHERE user_id = ? AND anchor = ?',
                (word_response.lower(), self.user_id, word_anchor.lower())
            )
        return cursor.rowcount

    def del_word_pair(self, word_anchor, word_response):
        with self.connection as c:
            cursor = c.execute(
                'DELETE FROM words WHERE user_id = ? AND anchor = ?',
                (self.user_id, word_anchor.lower())
            )
        return cursor.rowcount

    def update_words(self, words):
        with self.connection as c:
            for word in words:
                c.execute(
                    'UPDATE words SET correct = ?, incorrect = ?, '
                    'correct_letters = ?, incorrect_letters = ? '
                    'WHERE user_id = ? AND anchor = ?',
                    (word.correct, word.incorrect, word.correct_letters,
                     word.incorrect_letters, self.user_id, word.anchor)
                )
