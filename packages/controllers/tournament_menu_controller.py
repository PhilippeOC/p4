from ..utils.menu import Menu
from ..views.menu_view import MenuView
from .tournament_controller import TournamentController
from .import home_menu_controller


class TournamentMenuController:
    """ Menu pour gérer les tournois """
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def run(self):
        self.menu.title = "Gérer les tournois"
        self.menu.add("auto", "Créer un nouveau tournoi", TournamentController('new tournament'))
        self.menu.add("auto", "Reprendre un tournoi en cours", TournamentController('continue tournament'))
        self.menu.add("auto", "Ajouter un joueur à un tournoi", TournamentController('add player tournament'))
        self.menu.add("auto", "Menu précédent", home_menu_controller.HomeMenuController())
        self.menu.add("auto", "Quitter le programme", None)
        user_choice = self.view.get_user_choice()
        return user_choice
