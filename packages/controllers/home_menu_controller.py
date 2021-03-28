from ..utils.menu import Menu
from ..views.menu_view import MenuView
from .tournament_menu_controller import TournamentMenuController
from .player_menu_controller import PlayerMenuController
from .reports_menu_controller import ReportsMenuController


class HomeMenuController:
    """ Menu principal de l'application """
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def run(self):
        self.menu.title = "Accueil"
        self.menu.add("auto", "Gérer les tournois", TournamentMenuController())
        self.menu.add("auto", "Gérer les joueurs", PlayerMenuController())
        self.menu.add("auto", "Consulter les rapports", ReportsMenuController())
        self.menu.add("auto", "Quitter le programme", None)
        user_choice = self.view.get_user_choice()
        return user_choice
