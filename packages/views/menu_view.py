from .import in_out_view


class MenuView:
    def __init__(self, menu):
        self.menu = menu
        self.items = self.menu.items_menu()

    def __display_menu(self, clear=True):
        if clear:
            in_out_view.clear_console()
        in_out_view.title(self.menu.title)
        for key, menu_content in self.items.items():
            print(f"{key}: {menu_content.item_menu}")

    def get_user_choice(self, clear=True):
        while True:
            self.__display_menu(clear)
            print()
            choice = input("Votre choix: >> ")
            if self.menu.valid_key(choice):
                return self.items[str(choice)].action_menu
