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
    def _role_decorator(func):
        # сохраняет и изменяет выходные данные события с учетом роли
        # декоратор не особо тут и нужен, но пусть будет так
        def wrapper(*args, **kwargs):
            self = args[0]
            res = func(*args, **kwargs)
            if res:
                if self.role not in "manager":
                    # фразы клиентов не интересуют
                    res[1] = ''
                elif res[0] not in 'представление':
                    # сохраняем информацию о приветствии или прощании
                    self.polite_manager[res[0]] = True

                if res[0] in 'компания' or self.role in "manager":
                    # если компания или вежливый менеджер
                    # пишем событие большими буквами
                    res[0] = res[0].upper()

            return res
        return wrapper

    @_role_decorator
    def _event_greetings(self):
        return super()._event_greetings()

    @_role_decorator
    def _event_goodbye(self):
        return super()._event_goodbye()

    @_role_decorator
    def _event_introduce(self):
        return super()._event_introduce()

    @_role_decorator
    def _event_company(self):
        return super()._event_company()


if __name__ == '__main__':
    pass
