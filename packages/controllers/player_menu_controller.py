from ..utils.menu import Menu
from ..views.menu_view import MenuView
from .player_controller import PlayerController
from .import home_menu_controller


class PlayerMenuController():
    """ Menu pour gérer les joueurs """
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def run(self):
        self.menu.title = "Gérer les joueurs"
        self.menu.add("auto", "Ajouter des nouveaux joueurs", PlayerController())
        self.menu.add("auto", "Menu précédent", home_menu_controller.HomeMenuController())
        self.menu.add("auto", "Quitter le programme", None)
        user_choice = self.view.get_user_choice()
        return user_choice
