import os
import json
from dataclasses import dataclass

import config

PACK_DIR = os.path.join(config.BASE_DIR, 'data', 'packs')
MANIFEST_PATH = os.path.join(PACK_DIR, 'manifest.json')


@dataclass
class PackManager:
    db: object

    def add_pack(self, name):
        try:
            # Try .fr.json first, then .pl.json for backwards compat
            for ext in ['.fr.json', '.pl.json']:
                path = os.path.join(PACK_DIR, name + ext)
                if os.path.exists(path):
                    words = json.load(open(path, encoding='utf-8'))
                    self.insert_ignore(words)
                    return True
            return False
        except (FileNotFoundError, json.JSONDecodeError):
            return False

    def insert_ignore(self, words):
        for anchor, response in words.items():
            try:
                self.db.insert_word_pair(anchor.lower(), response.lower())
            except Exception:
                pass

    def get_packs(self):
        """Return packs sorted by priority from manifest, or alphabetically."""
        if os.path.exists(MANIFEST_PATH):
            manifest = json.load(open(MANIFEST_PATH))
            return sorted(
                manifest.keys(),
                key=lambda k: (manifest[k]['priority'], k)
            )
        return sorted(
            f.replace('.fr.json', '').replace('.pl.json', '')
            for f in os.listdir(PACK_DIR)
            if f.endswith('.json') and f != 'manifest.json'
        )

    def get_packs_detailed(self):
        """Return packs with word counts and priority info."""
        if os.path.exists(MANIFEST_PATH):
            manifest = json.load(open(MANIFEST_PATH))
            return sorted(
                [(name, info['count'], info['priority'])
                 for name, info in manifest.items()],
                key=lambda x: (x[2], x[0])
            )
        return [(name, '?', 99) for name in self.get_packs()]
