"""Модуль с классами всевозможных событий.

'приветствие' 'представление' 'имена' 'компания' 'прощание'
"""


import re

import nltk
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


class Event:
    """Суперкласс для всех событий."""

    def __init__(self):
        """Инициализирует переменные."""
        self.name = ''      # имя события
        self.result = ''    # результат, если случилось событие

    def check(self, text):
        """Проверка строки на событие."""
        pass


class EventGreetings(Event):
    """Событие: приветствие."""

    def __init__(self):
        """Инициализирует переменные."""
        super().__init__()
        self.name = 'приветствие'

    def check(self, text=''):
        """Проверка строки на событие."""
        if re.search(r'(?:добрый|здравствуйте)', text.lower(), flags=re.I):
            self.result = text
            return self.result


class EventIntroduce(Event):
    """Событие: представление."""

    def __init__(self):
        """Инициализирует переменные."""
        super().__init__()
        self.name = 'представление'

    def check(self, text=''):
        """Проверка строки на событие."""
        if re.search(r'меня.+зовут', text.lower(), flags=re.I):
            self.result = text
            return self.result


class EventAllNames(Event):
    """Событие: имена."""

    def __init__(self):
        """Инициализирует переменные."""
        super().__init__()
        self.name = 'имена'

    def check(self, text=''):
        """Ищем все имена в строке и возвращаем разделенные пробелом."""
        names = []
        for word in nltk.word_tokenize(text, language='russian'):
            for pars in morph.parse(word):
                if 'Name' in pars.tag and pars.score >= 0.3:
                    names.append(word)
        if names:
            self.result = ' '.join(names) if names else None
            return self.result


class EventCompany(Event):
    """Событие: компания."""

    def __init__(self):
        """Инициализирует переменные."""
        super().__init__()
        self.name = 'компания'

    def check(self, text=''):
        """Проверка строки на событие."""
        c = re.search(r'компания\s(.+бизнес)', text.lower(), flags=re.I)
        if c:
            self.result = c.group(1)
            return self.result


class EventGoodbye(Event):
    """Событие: прощание."""

    def __init__(self):
        """Инициализирует переменные."""
        super().__init__()
        self.name = 'прощание'

    def check(self, text=''):
        """Проверка строки на событие."""
        if re.search(
                r'(?:всего хорошего|до свидания|всего доброго)',
                text.lower(),
                flags=re.I):
            self.result = text
            return self.result


if __name__ == '__main__':
    pass
