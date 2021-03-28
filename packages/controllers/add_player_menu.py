from ..utils.menu import Menu
from ..views.menu_view import MenuView
from .import player_controller
from .import player_menu_controller


class AddPlayerMenu():
    """ Menu pour ajouter un autre joueur """

    def __init__(self, clear=True):
        self.menu = Menu()
        self.view = MenuView(self.menu)
        self.clear = clear

    def run(self):
        self.menu.title = "Ajouter des joueurs"
        self.menu.add("auto", "Ajouter un autre joueur", player_controller.PlayerController())
        self.menu.add("auto", "Menu précédent", player_menu_controller.PlayerMenuController())
        user_choice = self.view.get_user_choice(self.clear)
        return user_choice
