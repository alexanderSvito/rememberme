import os
import json
from dataclasses import dataclass

import config


PACK_DIR = os.path.join(
    config.BASE_DIR,
    'data',
    'packs'
)


@dataclass
class PackManager:
    db: object

    def add_pack(self, name):
        try:
            words = json.load(
                open(
                    os.path.join(
                        PACK_DIR,
                        name + '.pl.json'
                    )
                )
            )
            self.insert_ignore(words)
            return True
        except FileNotFoundError:
            return False

    def insert_ignore(self, words):
        for anchor, response in words.items():
            try:
                self.db.insert_word_pair(
                    anchor.lower(),
                    response.lower()
                )
            except:
                pass

    def get_packs(self):
        return [
            pack.replace('.pl.json', '')
            for pack in os.listdir(PACK_DIR)
        ]
