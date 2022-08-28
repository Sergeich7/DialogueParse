#
# Модуль с классом для парсинга одной строки
#

import pandas as pd

from IOData import data
from .events import EventGreetings, EventIntroduce,\
        EventAllNames, EventCompany, EventGoodbye


class RoleParser:

    def __init__(self, row: pd.Series):
        self.all_events = [     # все искомые события
            EventGreetings(),
            EventIntroduce(),
            EventAllNames(),
            EventCompany(),
            EventGoodbye()
        ]
        self.dlg_id, self.line_n, self.role, self.text = row
        self.polite_manager = {
                'приветствие': False,
                'прощание': False,
            }

    def parse(self):
        # проверяем на все возможные события в строке
        # запускаем все методы начинающиеся с 'event_'
        for event in self.all_events:
            # проверка одного события по названию метода event_ЧТоТоТАМ
            if event.check(self.text):
                # нашлось событие - выводим

                if self.role not in "manager":
                    # фразы клиентов не интересуют
                    event.result = ''
                elif event.name not in 'представление':
                    # сохраняем информацию о приветствии или прощании
                    self.polite_manager[event.name] = True

                if event.name in 'компания' or self.role in "manager":
                    # если компания или вежливый менеджер
                    # пишем событие большими буквами
                    event.name = event.name.upper()

                data.prn(self.dlg_id, self.line_n, self.role,
                    event.name, event.result)


if __name__ == '__main__':
    pass
