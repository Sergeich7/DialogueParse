"""DialogueParse - скрипт для парсинга диалогов.

При разработке программы использовалось ООП и библиотеки
NLTK, pymorphy2, re, Pandas

Программа извлекает из диалогов (test_data.csv) реплики с приветствием, с
прощаниями, с представлениями. Так-же извлекает имена людей и названия
компаний. Проверяет ВЕЖЛИВОСТЬ менеджера (должен поздороваться и попрощаться)

Мини ТЗ в файле tz.txt

Результаты работы выводятся в файл out_data.csv
Также выводятся на экран и копия в файл out_data.txt
"""

from dialogue import RoleParser, DialogueAnalyzer
from IOData import data


if __name__ == "__main__":

    dlg_id = None     # только начали разбирать диалоги
    dialogue = DialogueAnalyzer(dlg_id)

    for _, row in data.inp_d.iterrows():

        if dlg_id != row['dlg_id']:
            # Начался новый диалог

            if type(dlg_id) == int:
                # Статистика по предыдущему диалогу, если не 1ый заход
                dialogue.result()
                # просто ввожу пустую строку отделяющая диалоги
                data.prn('', '', '', '', '')

            dlg_id = row['dlg_id']
            dialogue = DialogueAnalyzer(row['dlg_id'])
            # просто шапка для каждого диалога
            data.prn('dlg_id', 'line_n', 'role', 'event', 'text')

        # разбираем каждую строку на события
        role_decoder = RoleParser(row)
        role_decoder.parse()
        # собираем нужную инфу из каждой строки для всего диалога
        dialogue.accumulate(role_decoder)

    # выводим результаты анализа последнего диалога
    dialogue.result()

    data.save()
