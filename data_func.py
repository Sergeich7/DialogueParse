#
# Модуль с процедурами для чтения/записи входных/выходных данных
#

import sys
import pandas as pd

# создаем выходной DataFrame
out_d = pd.DataFrame(columns=['dlg_id', 'line_n', 'role', 'event', 'text'])

# в файл выводим то-же, что и на экран
out_f = open('out_data.txt', 'w', encoding="utf8")


def prn_ln(dlg_id, line_n, role, event, text):
    # выводим и сохраняем результаты
    f_str = '{0:>6} {1:>6} {2:>7} {3:<12} {4}'.format(
        dlg_id, line_n, role, event, text)

    # на экран
    print(f_str)

    # в файл
    original_stdout = sys.stdout
    sys.stdout = out_f
    print(f_str)
    sys.stdout = original_stdout

    # в DataFrame
    if type(dlg_id) == int:
        global out_d
        add_d = pd.DataFrame({
                'dlg_id': [dlg_id], 'line_n': [line_n], 'role': [role],
                'event': [event], 'text': [text]
            })
        out_d = pd.concat([out_d, add_d], ignore_index=True)


def save_result():
    # сохранение результатов работы
    out_d.to_csv('out_data.csv', index=False, encoding="utf8")
    out_f.close()


if __name__ == '__main__':
    pass
