from typing import Union
import os
import json

class SimpleLang(object):
    def __init__(self, file = None):
        file = file if file else 'languages.json'
        self._load_from_file(file)
        self._current_lang = 'zh'

    def _load_from_file(self, file: str):
        path = os.path.dirname(os.path.abspath(__file__)) + '/' + file
        with open(path) as f:
            self.lang_dict = json.load(f)

    @property
    def current_lang(self):
        return self._current_lang

    def get_text(self, key):
        return self.lang_dict[self._current_lang][key]