import os
import json
import logging
from dataclasses import dataclass

from googletrans import Translator
import config

TRAN_DIR = os.path.join(
    config.BASE_DIR,
    'data',
    'tran'
)

logger = logging.getLogger(__file__)


@dataclass
class Translator:
    manager: object

    dictionary = json.load(open(
        os.path.join(
            TRAN_DIR,
            'pl_ru.json'
        )
    ))
    translator = Translator()

    def translate(self, word):
        word = word.strip()
        if word in self.dictionary:
            return self.dictionary[word]
        else:
            logger.info("Haven't found in dictionary: %s - making API call", word)
            return [self.translator.translate(word, dest='ru', src='pl').text]
