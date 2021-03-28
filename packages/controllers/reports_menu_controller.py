from ..utils.menu import Menu
from ..views.menu_view import MenuView
from .report_controller import ReportController
from .import home_menu_controller


class ReportsMenuController:
    """ Menu pour afficher les rapports """
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
        self.menu.add("auto", "Menu précédent", home_menu_controller.HomeMenuController())
        self.menu.add("auto", "Quitter le programme",  None)
        user_choice = self.view.get_user_choice()
        return user_choice
