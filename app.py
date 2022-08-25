#
# DialogueParse - скрипт для парсинга диалогов
#
# Использовались библиотеки: NLTK, pymorphy2, re, Pandas
#
# Программа извлекает из диалогов (test_data.csv) реплики с приветствием, с
# прощаниями, с представлениями. Так-же извлекает имена людей и названия
# компаний. Проверяет ВЕЖЛИВОСТЬ менеджера (должен поздороваться и попрощаться)
# Мини ТЗ в файле tz.txt
#
# Результаты работы выродятся в файл out_data.csv
# Также выводятся на экран и копия экрана в файл out_data.txt
#

from chk_func import chk_on
from data_func import inp_d, prn_ln, save_result

if __name__ == "__main__":

    dlg_id = None     # только начали разбирать диалоги
    manager_greetings = manager_goodbye = False

    for i, row in inp_d.iterrows():

        if dlg_id != row['dlg_id']:
            # Начался новый диалог

            if dlg_id:
                # Статистика по предидущему диалогу, если не 1ый заход
                if manager_greetings and manager_goodbye:
                    prn_ln(dlg_id, '', 'MANAGER', 'ВЕЖЛИВЫЙ',
                        "поздоровался и попрощался")
                prn_ln('', '', '', '', '')

            dlg_id = row['dlg_id']
            manager_greetings = manager_goodbye = False
            prn_ln('dlg_id', 'line_n', 'role', 'event', 'text')

        # проверяем все возможные события в строке
        # события могут быть
        # 'приветствие' 'представление' 'имена' 'компания' 'прощание'
        # правила обработки описаны в chk_on
        for key in chk_on:
            res = chk_on[key]['func'](
                row['text'], chk_on[key]['ptn'], chk_on[key]['ret_grp'])
            if res:
                role = row['role']
                event = key
                if key in ['приветствие', 'представление', 'прощание']:
                    res = ''    # не нужно вытаскивать фразу
                    if role in "manager":
                        if key in 'приветствие':
                            # менеджер в диалоге поприветствовал
                            manager_greetings = True
                        elif key in 'прощание':
                            # менеджер в диалоге попрощался
                            manager_goodbye = True
                        res = row['text']
                        # выделяем большими буквами MANAGER ПРОЩАНИЕ,
                        # то что нужно вытащить в задании
                        event = event.upper()
                        role = role.upper()
                elif key in 'компания':
                    # выделяем большими буквами КОМПАНИИ
                    event = event.upper()

                prn_ln(row['dlg_id'], row['line_n'], role, event, res)

    # результаты последнего диалога
    if manager_greetings and manager_goodbye:
        prn_ln(dlg_id, '', 'MANAGER', 'ВЕЖЛИВЫЙ', "поздоровался и попрощался")

    save_result()
