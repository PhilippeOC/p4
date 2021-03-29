from .import constants
from .import utils
from .import tournament_menu_controller
from ..views import in_out_view
from .match_controller import MatchController
from ..models.tournament_manager import TournamentManager
from ..models.player_manager import PlayerManager
from ..models.tournament import Tournament


class TournamentController:
    """ Création d'un nouveau tournoi
        Ajouter un joueur dans un tournoi
        Reprendre un tournoi non terminé
    """
    def __init__(self, item: str):
        self.item = item
        self.tm = TournamentManager()
        self.pm = PlayerManager()
        self.mc = MatchController()
        self.data_t = utils.tournaments_db_list
        self.data_p = utils.players_db_list
        self.title = ""

    def run(self):
        if self.item == 'new tournament':
            self.title = "Création d'un tournoi"
            self.data_t.append(self.add_tournament())
            return tournament_menu_controller.TournamentMenuController()
        elif self.item == 'add player tournament':
            less_than_8 = self.less_than_eight()
            if less_than_8:
                num = utils.choose_tournament(less_than_8, "Liste des tournois de moins de 8 joueurs")
                t = self.tm.create_tournament(less_than_8[num-1])
                while True:
                    if self.choose_player(t):
                        break
                self.disp_players(t)
                in_out_view.wait()
                return tournament_menu_controller.TournamentMenuController()
            else:
                while True:
                    in_out_view.clear_console()
                    if in_out_view.come_back("Tous les tournois sont complets."):
                        break
                return tournament_menu_controller.TournamentMenuController()

        elif self.item == 'continue tournament':
            no_finish = self.t_no_finished()
            num_t = utils.choose_tournament(no_finish, "Liste des tournois en cours")
            t = self.tm.create_tournament(no_finish[num_t-1])
            if self.tournament_not_ok(t):
                return tournament_menu_controller.TournamentMenuController()
            nb_turn = len(t.round_list) + 1
            while nb_turn <= t.nb_turns:
                if len(t.round_list) == 0:
                    if self.mc.match_making_first_round(t):
                        break
                    self.mc.end_round(t, nb_turn)
                    self.update_data_t(t)
                    nb_turn += 1

                in_out_view.wait()
                if self.mc.match_making_other_rounds(t, nb_turn):
                    break
                self.mc.end_round(t, nb_turn)
                self.update_data_t(t)
                nb_turn += 1
            if nb_turn == t.nb_turns + 1:
                t.finished = True
                self.update_data_t(t)
            return tournament_menu_controller.TournamentMenuController()

    def tournament_not_ok(self, tournament: dict) -> bool:
        """verifie que le tournois a bien un nombre pair non nul de joueurs """
        nb_players = len(tournament.players_id_list)
        if nb_players % 2 == 1:
            while True:
                in_out_view.clear_console()
                if in_out_view.come_back(f"Il y a {nb_players} joueurs dans ce Tournoi:"
                                         f"{tournament.name} à {tournament.place} le {tournament.date}. \n"
                                         f"Il doit contenir un nombre pair de joueurs. \n"):
                    break
            return True
        if nb_players == 0:
            while True:
                in_out_view.clear_console()
                if in_out_view.come_back(f"Il n'y a aucun joueur dans ce tournoi:"
                                         f"{tournament.name} à {tournament.place} le {tournament.date}."):
                    break
            return True

    def update_data_t(self, tournament: dict):
        """mise à jour des données du tournois"""
        for num, tournament_data in enumerate(self.data_t):
            trnt = self.tm.create_tournament(tournament_data)
            if trnt.identifier == tournament.identifier:
                self.data_t[num] = tournament.serialize()
                break

    def t_no_finished(self) -> list:
        """retourne la liste des tournois non terminés"""
        no_finished = []
        for tournament in self.data_t:
            t = self.tm.create_tournament(tournament)
            if not t.finished:
                no_finished.append(t.serialize())
        return no_finished

    def p_already_in_t(self, tournament: dict, player: dict) -> bool:
        if str(player.identifier) in tournament.players_id_list:
            return True

    def choose_player(self, tournament: dict):
        self.disp_players(tournament)
        in_out_view.display_title("Choix du joueur à ajouter", False)
        nb_items = in_out_view.display_players_aplhabetic(utils.disp_players_alpha(self.data_p), clear=False)
        num_p = in_out_view.get_number_entry("Entrer le N° du joueur", nb_items)

        if num_p:
            self.data_p = utils.disp_players_alpha(self.data_p)
            p = self.pm.create_player(self.data_p[num_p-1])
            if tournament.players_id_list:
                if self.p_already_in_t(tournament, p):
                    while True:
                        in_out_view.clear_console()
                        self.disp_players(tournament)
                        if in_out_view.come_back(f"{p.firstname} {p.lastname} est déjà dans le tournoi!"):
                            break
                    return tournament_menu_controller.TournamentMenuController()

            tournament.players_id_list.append(str(p.identifier))
            self.update_data_t(tournament)

            if len(tournament.players_id_list) == 8:
                while True:
                    in_out_view.clear_console()
                    self.disp_players(tournament)
                    if in_out_view.come_back("Le tournoi est complet."):
                        break
                return tournament_menu_controller.TournamentMenuController()
            return True
        else:
            return False

    def disp_players(self, tournament: dict):
        subtitle = f"Tournoi: {tournament.name} à {tournament.place} le {tournament.date}"
        play_list = []
        if len(tournament.players_id_list) != 0:
            for num, player in enumerate(tournament.players_id_list):
                play = utils.id_player_to_player(tournament.players_id_list[num], self.data_p)
                play_list.append((play.lastname, play.firstname))
            in_out_view.display_players_less8(sorted(play_list), subtitle)
        else:
            in_out_view.subtitle(subtitle, clear=True)

    def less_than_eight(self):
        """retourne la liste des tournois ayant moins de 8 joueurs"""
        less_than_8 = []
        for tournament in self.data_t:
            t = self.tm.create_tournament(tournament)
            if len(t.players_id_list) < 8:
                less_than_8.append(t.serialize())
        return less_than_8

    def add_tournament(self):
        tournament_data = {}
        for key, data in constants.ITEMS_TOURNAMENTS.items():
            if key == 'nb_turns':
                tournament_data[key] = in_out_view.get_user_entry(self.title, "", data, '4')
            elif key == 'description':
                tournament_data[key] = in_out_view.get_user_entry(self.title, "", data, ' ')
            else:
                tournament_data[key] = in_out_view.get_user_entry(self.title, "", data, None)
        return self.create_tournament(tournament_data)

    def create_tournament(self, tournament_data: dict):
        try:
            t = self.tm.create_tournament(tournament_data)
            return t.serialize()
        except Tournament.Error as err:
            return self.error_entries(tournament_data, err.args[1])

    def error_entries(self, tournament_data: dict, errors: dict):
        for item_key, message in errors.items():
            ask = constants.ITEMS_TOURNAMENTS[item_key]
            if item_key == 'nb_turns':
                tournament_data[str(item_key)] = in_out_view.get_user_entry(self.title, message, ask, '4')
            else:
                tournament_data[str(item_key)] = in_out_view.get_user_entry(self.title, message, ask, None)
        return self.create_tournament(tournament_data)
