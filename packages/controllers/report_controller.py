from ..models.tournament_manager import TournamentManager
from .import reports_menu_controller
from ..views import in_out_view
from .import utils


class ReportController:
    """ Création des rapports:
    - liste des acteurs par ordre alphabétique et par classement
    - liste des joueurs d'un tournoi
    - liste de tous les tournois
    - liste de tous les tours d'un tournoi
    - liste de tous les matchs d'un tournoi
     """

    def __init__(self, report):
        self.report = report
        self.tm = TournamentManager()
        self.data_t = utils.tournaments_db_list
        self.data_p = utils.players_db_list

    def run(self):
        if self.report == 'players alphabetical':
            while True:
                in_out_view.display_players_aplhabetic(utils.disp_players_alpha(self.data_p))
                if in_out_view.come_back():
                    break
            return reports_menu_controller.ReportsMenuController()

        elif self.report == 'players rank':
            while True:
                in_out_view.display_players_rank(utils.disp_players_rank(self.data_p))
                if in_out_view.come_back():
                    break
            return reports_menu_controller.ReportsMenuController()

        elif self.report == 'players in tournament':
            num = utils.choose_tournament(self.data_t)
            t = self.tm.create_tournament(self.data_t[num-1])
            subtitle = f"Tournoi: {t.name} à {t.place} le {t.date}"
            if t.players_id_list:
                data = []
                for uuid_id in t.players_id_list:
                    play = utils.id_player_to_player(uuid_id, self.data_p)
                    data.append(play.serialize())
                data_tuple = (utils.disp_players_alpha(data), utils.disp_players_rank(data))
                while True:
                    in_out_view.display_players_in_tournaments(data_tuple, subtitle)
                    if in_out_view.come_back():
                        break
                return reports_menu_controller.ReportsMenuController()
            else:
                while True:
                    in_out_view.display_tournaments(self.data_t, "Liste des tournois")
                    if in_out_view.come_back("Il n'y a pas encore de joueur dans ce tournoi.\n"):
                        break
                return reports_menu_controller.ReportsMenuController()

        elif self.report == 'tournaments list':
            while True:
                in_out_view.display_tournaments(self.data_t)
                if in_out_view.come_back():
                    break
            return reports_menu_controller.ReportsMenuController()

        elif self.report == 'tours list':
            num = utils.choose_tournament(self.data_t)
            t = self.tm.create_tournament(self.data_t[num-1])
            subtitle = f"Tournoi: {t.name} à {t.place} le {t.date}"

            if t.round_list:
                ready_to_disp = self.format_round_for_display(t.round_list)
                while True:
                    in_out_view.display_tours(ready_to_disp, subtitle)
                    if in_out_view.come_back():
                        break
                return reports_menu_controller.ReportsMenuController()
            else:
                while True:
                    in_out_view.display_tournaments(self.data_t, "Liste des tournois")
                    if in_out_view.come_back("Il n'y a pas encore de tour dans ce tournoi.\n"):
                        break
                return reports_menu_controller.ReportsMenuController()

        elif self.report == 'matchs list':
            num = utils.choose_tournament(self.data_t)
            t = self.tm.create_tournament(self.data_t[num-1])
            subtitle = f"Tournoi: {t.name} à {t.place} le {t.date}"
            if t.round_list:
                match_to_disp = []
                matchs_list = self.tm.find_matchs(t.identifier)

                for num_round, match_list in enumerate(matchs_list):
                    if match_list['matchs_list']:
                        match_to_disp.append(utils.match_player_score(match_list['matchs_list']))
                    else:
                        while True:
                            in_out_view.display_tournaments(self.data_t, "Liste des tournois")
                            if in_out_view.come_back("Il n'y a pas encore de match dans ce tournoi\n"):
                                break
                        return reports_menu_controller.ReportsMenuController()
                while True:
                    in_out_view.display_matchs(match_to_disp, None, subtitle)
                    if in_out_view.come_back():
                        break
                return reports_menu_controller.ReportsMenuController()
            else:
                while True:
                    in_out_view.display_tournaments(self.data_t, "Liste des tournois")
                    if in_out_view.come_back("Il n'y a pas encore de tour, donc de match, dans ce tournoi.\n"):
                        break
                return reports_menu_controller.ReportsMenuController()

    def format_round_for_display(self, round_list: list) -> list:
        turns_list = []
        for num, turns in enumerate(round_list):
            turns_dict = {}
            turns_dict['name'] = round_list[num]['name']
            turns_dict['start_datetime'] = round_list[num]['start_datetime']
            turns_dict['end_datetime'] = round_list[num]['end_datetime']
            turns_list.append(turns_dict)
        return turns_list
