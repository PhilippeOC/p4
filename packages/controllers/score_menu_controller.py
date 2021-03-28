from ..utils.menus import Menu
from ..views.menu_view import MenuView
from .tournament_controller import TournamentController
from .tournament_menu_controller import TournamentMenuController
from .match_controller import MatchController


class ScoreMenuController:
    """ Menu pour saisir les scores """
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)
        self.score = TournamentController('continue tournament')

    def run(self):
        self.menu.title = "Score des matchs"
        self.menu.add("auto", "Entrer les scores des matchs", MatchController(self.score))
        self.menu.add("auto", "Menu précédent", TournamentMenuController())
        user_choice = self.view.get_user_choice(False)
        return user_choice
