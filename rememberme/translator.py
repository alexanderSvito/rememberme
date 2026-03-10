import os
import json
import logging
from dataclasses import dataclass

import config

TRAN_DIR = os.path.join(config.BASE_DIR, 'data', 'tran')
logger = logging.getLogger(__name__)


@dataclass
class WordTranslator:
    manager: object

    def __post_init__(self):
        dict_path = os.path.join(TRAN_DIR, 'en_fr.json')
        if os.path.exists(dict_path):
            with open(dict_path, encoding='utf-8') as f:
                self.dictionary = json.load(f)
        else:
            self.dictionary = {}

    def translate(self, word):
        word = word.strip().lower()
        # Check exact match
        if word in self.dictionary:
            val = self.dictionary[word]
            return val if isinstance(val, list) else [val]

        # Check case-insensitive
        for key, val in self.dictionary.items():
            if key.lower() == word:
                return val if isinstance(val, list) else [val]

        return None
