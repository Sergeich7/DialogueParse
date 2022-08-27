#
# Модуль с классом для чтения/записи входных/выходных данных
#

import sys
import pandas as pd


class InpOutData():

    def __init__(self):
        # читаем входные данные
        self.inp_d = pd.read_csv("test_data.csv", encoding="utf8")
        # создаем выходной DataFrame
        self.out_d = pd.DataFrame(columns=['dlg_id', 'line_n', 'role', 'event', 'text'])
        # в файл выводим то-же, что и на экран
        self.out_f = open('out_data.txt', 'w', encoding="utf8")

    def prn(self, dlg_id, line_n, role, event, text):
        # выводим и сохраняем результаты
        f_str = '{0:>6} {1:>6} {2:>7} {3:<12} {4}'.format(
            dlg_id, line_n, role, event, text)

        # в файл
        original_stdout = sys.stdout
        sys.stdout = self.out_f
        print(f_str)
        sys.stdout = original_stdout

        # на экран
        if event.isupper():
            # подчеркнем важные строки
            f_str = f'\033[4m{f_str}\033[0m'
        print(f_str)

        # в DataFrame
        if type(dlg_id) == int:
            self.add_d = pd.DataFrame({
                    'dlg_id': [dlg_id], 'line_n': [line_n], 'role': [role],
                    'event': [event], 'text': [text]
                })
            self.out_d = pd.concat([self.out_d, self.add_d], ignore_index=True)

    def save(self):
        # сохранение результатов работы
        self.out_f.close()
        self.out_d.to_csv('out_data.csv', index=False, encoding="utf8")


data = InpOutData()

if __name__ == '__main__':
    pass
