#
# Модуль с классом определения событий
#
# каждое событие, если находится в строке, возвращает список
# ['Название', 'СтрокаДанных'], иначе None
#
# Название - 'приветствие' 'представление' 'имена' 'компания' 'прощание'
#

import re

import nltk
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


class Events():

    def __init__(self):
        self.text = ''
        self.events = {
            'приветствие':      self._event_greetings,
            'представление':    self._event_introduce,
            'имена':            self._event_all_names,
            'компания':         self._event_company,
            'прощание':         self._event_goodbye,
        }

    def _event_greetings(self):
        # проверка на приветствие
        if re.search(r'(?:добрый|здравствуйте)',
                self.text.lower(), flags=re.I):
            return ['приветствие', self.text]
        return None

    def _event_introduce(self):
        # проверка на представление
        if re.search(r'меня.+зовут', self.text.lower(), flags=re.I):
            return ['представление', self.text]
        return None

    def _event_all_names(self):
        # находим все имена в строке и возвращаем разделенные пробелом
        # или возвращает None, если имен в строке нет
        names = []
        for word in nltk.word_tokenize(self.text, language='russian'):
            for pars in morph.parse(word):
                if 'Name' in pars.tag and pars.score >= 0.3:
                    names.append(word)
        return ['имена', ' '.join(names)] if names else None

    def _event_company(self):
        # проверка на компания
        c = re.search(r'компания\s(.+бизнес)', self.text.lower(), flags=re.I)
        return ['компания', c.group(1)] if c else None

    def _event_goodbye(self):
        # проверка на представление
        if re.search(r'(?:всего хорошего|до свидания|всего доброго)',
                self.text.lower(), flags=re.I):
            return ['прощание', self.text]
        return None


if __name__ == '__main__':
    pass
