#
# Модуль с классом для парсинга одной строки
#

import pandas as pd

from dialogue import Events
from IOData import data


class RoleParser(Events):

    def __init__(self, row: pd.Series):
        super().__init__()
        self.dlg_id, self.line_n, self.role, self.text = row
        self.polite_manager = {
                'приветствие':  False,
                'прощание':  False,
            }

    def parse(self):
        # проверяем на все возможные события в строке
        # запускаем все методы начинающиеся с 'event_'
        for event in self.events:
            # проверка одного события по названию метода event_ЧТоТоТАМ
            res = self.events[event]()
            if res:
                # нашлось событие - выводим
                data.prn(self.dlg_id, self.line_n, self.role, res[0], res[1])

    @staticmethod
    def _polite_decorator(func):
        # декоратор для событий менеджеров
        def wrapper(*args, **kwargs):
            self = args[0]
            res = func(*args, **kwargs)
            if res:
                if self.role in "manager":
                    if res[0] not in 'представление':
                        self.polite_manager[res[0]] = True
                    res[0] = res[0].upper()
                else:
                    res[1] = ''
            return res
        return wrapper

    @_polite_decorator
    def _event_greetings(self):
        return super()._event_greetings()

    @_polite_decorator
    def _event_goodbye(self):
        return super()._event_goodbye()

    @_polite_decorator
    def _event_introduce(self):
        return super()._event_introduce()

    def _event_company(self):
        # переопределяем с учетом задания
        res = super()._event_company()
        if res:
            res[0] = str(res[0]).upper()
        return res


if __name__ == '__main__':
    pass
