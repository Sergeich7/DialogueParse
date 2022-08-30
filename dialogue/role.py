"""Модуль с классом для парсинга одной строки."""

import pandas as pd

from IOData import data
from .events import EventGreetings, EventIntroduce,\
        EventAllNames, EventCompany, EventGoodbye


class RoleParser:
    """Класс парсинга одной строки."""

    def __init__(self, row: pd.Series):
        """Инициализирует переменные."""
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
        """Проверяем на все возможные события в строке."""
        for event in self.all_events:
            # проверка одного события по названию метода event_ЧТоТоТАМ
            if event.check(self.text):
                # нашлось событие - выводим

                if self.role in "manager" and\
                        event.name not in 'представление':
                    # сохраняем информацию о приветствии или прощании менеджера
                    self.polite_manager[event.name] = True

                if self.role not in "manager" and\
                        event.name not in ['компания', 'имена']:
                    # блокируем фразы/результат событий не относящиеся к делу
                    event.result = ''

                if event.name in 'компания' or\
                        self.role in "manager":
                    # все такие события:
                    # a) Извлекать реплики с приветствием, где менеджер
                    #    поздоровался.
                    # b) Извлекать реплики, где менеджер представил себя.
                    # c) Извлекать имя менеджера.
                    # d) Извлекать название компании.
                    # e) Извлекать реплики, где менеджер попрощался.
                    # выделяем заглавными буквами
                    self.role = self.role.upper()
                    event.name = event.name.upper()
                    event.result = event.result.upper()

                data.prn(
                    self.dlg_id, self.line_n, self.role,
                    event.name, event.result
                    )


if __name__ == '__main__':
    pass
