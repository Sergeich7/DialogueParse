#
# Модуль с процедурами для парсинга строки
#

import re

import nltk
import pymorphy2

prob_thresh = 0.3
morph = pymorphy2.MorphAnalyzer()


def get_all_names(text='', *argv):
    # находим все имена в строке и возвращаем разделенные пробелом
    # или возвращает None, если имен в строке нет
    names = []
    for word in nltk.word_tokenize(text, language='russian'):
        for pars in morph.parse(word):
            if 'Name' in pars.tag and pars.score >= prob_thresh:
                names.append(word)
    return ' '.join(names) if names else None


def find_ptn(text='', ptn='', ret_grp=0):
    # ищет шаблон в строке и возвращает
    # если найдет что-то всю строку или только 1ую совпадающую группу
    # или None
    c = re.search(ptn.lower(), text.lower(), flags=re.I)
    return c.group(ret_grp) if c else None


chk_on = {
    # func      - функция для обработка конкретного события
    # ptn       - шаблон, если функция работает на основе RegExp
    # ret_grp   - номер группы поиска, которую возвращает функция
    'приветствие': {    # проверка на приветствие в строке
        'func':     find_ptn,
        'ptn':      r'(?:добрый|здравствуйте)',
        'ret_grp':  0, },
    'представление': {  # проверка на представление в строке
        'func':     find_ptn,
        'ptn':      r'меня.+зовут',
        'ret_grp':  0, },
    'имена': {          # вытаскиваем все имена из строки
        'func':     get_all_names,
        'ptn':      r'',
        'ret_grp':  0, },
    'компания': {       # вытаскиваем название компании из строки
        'func':     find_ptn,
        'ptn':      r'компания\s(.+бизнес)',
        'ret_grp':  1, },
    'прощание': {       # проверка на прощание в строке
        'func': find_ptn,
        'ptn': r'(?:всего хорошего|до свидания|всего доброго)',
        'ret_grp':  0, },
}

if __name__ == '__main__':
    # проверочка идеи
    text = "Меня зовут ангелина компания диджитал бизнес звоним вам по " \
        "поводу продления лицензии а мы с серым у вас скоро срок заканчивается"
    for word in nltk.word_tokenize(text, language='russian'):
        for pars in morph.parse(word):
#            print(pars.tag)
            if 'Orgn' in pars.tag and pars.score >= prob_thresh:
                print(word)

    pass
