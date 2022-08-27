#
# Модуль с классом для разбора диалога
#

from dialogue import RoleParser
from IOData import data


class DialogueAnalyzer():
    # Класс во время всего диалога собирает информация
    # по запросу анализирует и выдает результаты по всему диалогу

    def __init__(self, dlg_id):
        self.dlg_id = dlg_id
        self.polite_manager = {
                'приветствие':  False,
                'прощание':  False,
            }

    def accumulate(self, rp: RoleParser):
        # собираем информацию о приветствиях и прощаниях менеджера
        # из каждой строки диалога

        self.polite_manager['приветствие'] =\
            self.polite_manager['приветствие'] or\
            rp.polite_manager['приветствие']

        self.polite_manager['прощание'] =\
            self.polite_manager['прощание'] or\
            rp.polite_manager['прощание']

    def result(self):
        # анализируем информацию и выдаем результат
        if self.polite_manager['приветствие'] and\
                self.polite_manager['прощание']:
            data.prn(self.dlg_id, '', 'manager', 'ВЕЖЛИВЫЙ',
                "поздоровался и попрощался")


if __name__ == "__main__":
    pass
