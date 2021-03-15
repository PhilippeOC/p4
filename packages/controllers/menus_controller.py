
from .tournament_controller import TournamentController
from .report_controller import ReportController
from .player_controller import PlayerController
from .match_controller import MatchScore
from ..utils.menus import Menu
from ..views.menu_view import MenuView


class HomeMenuController:
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


class TournamentMenuController:
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def run(self):
        self.menu.title = "Gérer les tournois"
        self.menu.add("auto", "Créer un nouveau tournoi", TournamentController('new tournament'))
        self.menu.add("auto", "Reprendre un tournoi en cours", TournamentController('continue tournament'))
        self.menu.add("auto", "Ajouter un joueur à un tournoi", TournamentController('add player tournament'))
        self.menu.add("auto", "Menu précédent", HomeMenuController())
        self.menu.add("auto", "Quitter le programme", None)
        user_choice = self.view.get_user_choice()
        return user_choice


class PlayerMenuController():
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def run(self):
        self.menu.title = "Gérer les joueurs"
        self.menu.add("auto", "Ajouter des nouveaux joueurs", PlayerController('add new players'))
        #self.menu.add("auto", "Modifier des joueurs", PlayerController('modif players'))
        self.menu.add("auto", "Menu précédent", HomeMenuController())
        self.menu.add("auto", "Quitter le programme", None)
        user_choice = self.view.get_user_choice()
        return user_choice


class ReportsMenuController:
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def run(self):
        self.menu.title = "Rapports"
        self.menu.add("auto", "Liste des acteurs par ordre alphabétique", ReportController('players alphabetical'))
        self.menu.add("auto", "Liste des acteurs par classement", ReportController('players rank'))
        self.menu.add("auto", "Liste des joueurs d'un tournoi", ReportController('players in tournament'))
        self.menu.add("auto", "Liste de tous les tournois", ReportController('tournaments list'))
        self.menu.add("auto", "Liste de tous les tours d'un tournoi", ReportController('tours list'))
        self.menu.add("auto", "Liste de tous les matchs d'un tournoi", ReportController('matchs list'))
        self.menu.add("auto", "Menu précédent", HomeMenuController())
        self.menu.add("auto", "Quitter le programme",  None)
        user_choice = self.view.get_user_choice()
        return user_choice


class AddPlayerMenuController:
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def run(self):
        self.menu.title = "Ajouter un joueur à un tournoi"
        self.menu.add("auto", "Joueur dans la base de données", TournamentController('player in bd'))
        self.menu.add("auto", "Nouveau joueur", PlayerController('new player'))
        self.menu.add("auto", "Menu précédent", TournamentMenuController())
        self.menu.add("auto", "Quitter le programme", None)
        user_choice = self.view.get_user_choice(False)
        return user_choice


class ScoreMenuController:
    def __init__(self):
        self.menu = Menu()
        self.view = MenuView(self.menu)
        self.score = TournamentController('continue tournament')
        #self.match = Score(self.score)

    def run(self):
        self.menu.title = "Score des matchs"
        self.menu.add("auto", "Entrer les scores des matchs", MatchScore(self.score))
        self.menu.add("auto", "Menu précédent", TournamentMenuController())
        #self.menu.add("auto", "Quitter le programme", None)
        user_choice = self.view.get_user_choice(False)
        return user_choice




def player_add_menu():
    item_menu = {}
    title = "Ajouter des joueurs"
    item_menu['Ajouter un autre joueur'] = PlayerController('add new players')
    item_menu['Menu précédent'] = PlayerMenuController()
    return CustomMenuChoice(title, item_menu)


"""def input_scores():
    item_menu = {}
    title = "Score des matchs"
    item_menu['Entrer les scores des matchs'] = disp_toto()
    item_menu['Menu précédent'] = TournamentMenuController()
    return CustomMenuChoice(title, item_menu, False)
"""

class CustomMenuChoice():
    def __init__(self, title: str, item_menu: dict, clear=True):
        self.title = title
        self.clear = clear
        self.item_menu = item_menu
        self.menu = Menu()
        self.view = MenuView(self.menu)

    def run(self):
        self.menu.title = self.title
        for key, value in self.item_menu.items():
            self.menu.add("auto", key, value)
        user_choice = self.view.get_user_choice(self.clear)
        return user_choice




