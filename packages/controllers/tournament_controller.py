from .import constants
from .import utils
from .import menus_controller
from ..views import in_out_view
from .match_controller import MatchScore
from ..models.tournament_manager import TournamentManager
from ..models.player_manager import PlayerManager
from ..models.tournament import Tournament
from ..models.turn import Round
from ..models.match import Match


class TournamentController:
    def __init__(self, item):
        self.item = item
        self.tm = TournamentManager()
        self.pm = PlayerManager()
        self.ms = MatchScore()
        self.data_t = utils.tournaments_db_list
        self.data_p = utils.players_db_list
        self.title = ""

    def run(self):
        if self.item == 'new tournament':
            self.title = "Création d'un tournoi"
            self.data_t.append(self.add_tournament())
            return menus_controller.TournamentMenuController()
        elif self.item == 'add player tournament':
            less_than_8 = self.less_than_eight()
            num = utils.choose_tournament(less_than_8, "Liste des tournois de moins de 8 joueurs")
            t = self.tm.create_tournament(less_than_8[num-1])
            while True:
                if self.choose_player(t):
                    break
            self.disp_players(t)
            in_out_view.wait()
            return menus_controller.TournamentMenuController()
        elif self.item == 'continue tournament':
            no_finish = self.t_no_finished()
            num_t = utils.choose_tournament(no_finish, "Liste des tournois en cours")
            t = self.tm.create_tournament(no_finish[num_t-1])
            if self.tournament_not_ok(t):
                return menus_controller.TournamentMenuController()

            if len(t.round_list) == 0:
                self.create_round("Round 1", t)
                if self.ms.choose_to_enter_score(t) == 2:
                    return menus_controller.TournamentMenuController()
                
                t.round_list[0]['match_list'] = self.ms.add_matchs_rd1(t)
                self.update_data_t(t)

            #self.ms.sum_of_scores(t)
            #print('tm', self.tm.find_matchs(t.identifier))

            in_out_view.wait()

            return menus_controller.TournamentMenuController()

    def create_round(self, name: str, t):
        rd = {}
        self.rd = Round(name)
        rd['name'] = name
        t.round_list.append(self.rd.create_round())

    def tournament_not_ok(self, t):
        """verifie que le tournois a bien un nombre pair non nul de joueurs """
        nb_players = len(t.players_id_list)
        if nb_players % 2 == 1:
            while True:
                in_out_view.clear_console()
                if in_out_view.come_back(f"Il y a {nb_players} joueurs dans ce Tournoi: {t.name} à {t.place} le {t.date}. \n"
                                         f"Il doit contenir un nombre pair de joueurs. \n"):
                    break
            return True
        if nb_players == 0:
            while True:
                in_out_view.clear_console()
                if in_out_view.come_back(f"Il n'y a aucun joueur dans ce tournoi: {t.name} à {t.place} le {t.date}."):
                    break
            return True

    def update_data_t(self, t):
        """mise à jour des données du tournois"""
        for num, tournament in enumerate(self.data_t):
            trnt = self.tm.create_tournament(tournament)
            #print(num, trnt.identifier)
            if trnt.identifier == t.identifier:
                self.data_t[num] = t.serialize()
                break

    def t_no_finished(self):
        """retourne la liste des tournois non terminés"""
        no_finished = []
        for tournament in self.data_t:
            t = self.tm.create_tournament(tournament)
            if not t.finished:
                no_finished.append(t.serialize())
        return no_finished

    def p_already_in_t(self, t, p):
        if str(p.identifier) in t.players_id_list:
            return True

    def choose_player(self, t):
        if t.players_id_list:
            self.disp_players(t)
        in_out_view.display_title("Choix du joueur à ajouter", False)
        nb_items = in_out_view.display_players_aplhabetic(utils.disp_players_alpha(self.data_p), clear=False)
        num_p = in_out_view.get_number_entry("Entrer le N° du joueur", nb_items)

        if num_p:
            p = self.pm.create_player(self.data_p[num_p-1])
            if t.players_id_list:
                if self.p_already_in_t(t, p):
                    while True:
                        in_out_view.clear_console()
                        self.disp_players(t)
                        if in_out_view.come_back(f"{p.firstname} {p.lastname} est déjà dans le tournoi!"):
                            break
                    return menus_controller.TournamentMenuController()
            t.players_id_list.append(str(p.identifier))

            if len(t.players_id_list) == 8:
                while True:
                    in_out_view.clear_console()
                    self.disp_players(t)
                    if in_out_view.come_back("Le tournoi est complet."):
                        break
                return menus_controller.TournamentMenuController()
            return True
        else:
            return False

    def disp_players(self, t):
        subtitle = f"Tournoi: {t.name} à {t.place} le {t.date}"
        play_list = []
        for num, player in enumerate(t.players_id_list):
            play = utils.id_player_to_player(t.players_id_list[num], self.data_p)
            play_list.append((play.lastname, play.firstname))
        in_out_view.display_players_less8(sorted(play_list), subtitle)

    def less_than_eight(self):
        """retourne la liste des tournois ayant moins de 8 joueurs"""
        less_than_8 = []
        for tournament in self.data_t:
            t = self.tm.create_tournament(tournament)
            if len(t.players_id_list) == 0:
                less_than_8.append(t.serialize())
            elif len(t.players_id_list) < 8:
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

