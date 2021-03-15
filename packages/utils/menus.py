from collections import namedtuple


class Menu:
    def __init__(self):
        self.__menu_entries = {}
        self.__title = ""
        self.__auto_num = 1

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__title = title

    def add(self, key: str,  item_menu: str, action_menu):
        if key == "auto":
            key = str(self.__auto_num)
            self.__auto_num += 1
        menu_content = namedtuple('menu_content', ['item_menu', 'action_menu'])
        self.__menu_entries[str(key)] = menu_content(item_menu, action_menu)

    def items_menu(self):
        return self.__menu_entries

    def valid_key(self, choice: str):
        return choice in self.__menu_entries
