
from .import utils
from ..views import in_out_view
from ..models.tournament_manager import TournamentManager
from ..models.player_manager import PlayerManager
from ..models.match import Match
from .import menus_controller


class MatchScore:
    def __init__(self):
        self.tm = TournamentManager()
        self.pm = PlayerManager()
       
        self.data_t = utils.tournaments_db_list
        self.data_p = utils.players_db_list

    def matchs_to_play_rd1(self, t):
        play_by_rank = self.player_by_rank(t)
        value = len(play_by_rank) // 2
        lower_list = play_by_rank[0:value]
        upper_list = play_by_rank[value: len(play_by_rank)]
        matchs_to_play = []
        for num, player in enumerate(lower_list):
            matchs_to_play.append((lower_list[num], upper_list[num]))
        in_out_view.disp_matchs_to_do(matchs_to_play, "round 1")
        return matchs_to_play

    def player_by_rank(self, t):
        """ retourne la liste des joueurs du round 1 classés par rank croissant:
            ranking, lastname, firstname, identifier """
        play_data_list = []
        for id_players in t.players_id_list:
            play_data = {}
            play_data['ranking'] = utils.id_player_to_player(id_players, self.data_p).ranking
            play_data['lastname'] = utils.id_player_to_player(id_players, self.data_p).lastname
            play_data['firstname'] = utils.id_player_to_player(id_players, self.data_p).firstname
            play_data['identifier'] = str(utils.id_player_to_player(id_players, self.data_p).identifier)
            play_data_list.append(play_data)
        return utils.disp_players_rank(play_data_list)

    def ask_enter_score(self):
        in_out_view.disp_ask_enter_score()
        return in_out_view.get_number_entry("Votre choix", 2)

    def input_score(self, num_match: int, play_1: dict, play_2: dict):
        in_out_view.display_title("Entrer les scores des matchs", False)
        in_out_view.disp_one_match(num_match, play_1, play_2)
        in_out_view.to_enter_the_scores()
        return in_out_view.get_number_entry("Entrer le résultat du match", 2)


    def match_player_score(self, num, play_1, play_2):
        winner = 1
        loser = 0
        tie_game = 0.5
        if num == 1:
            return ([play_1['identifier'], winner], [play_2['identifier'], loser])
        elif num == 2:
            return ([play_1['identifier'], loser], [play_2['identifier'], winner])
        elif num == 3:
            return ([play_1['identifier'], tie_game], [play_2['identifier'], tie_game])

    def sum_of_scores(self, t):
        self.tm.create_tournament(t.serialize())
        sum_scores = {}
        for num, player in enumerate(t.players_id_list):
            sum_p = 0
            for matchs in self.tm.find_matchs(t.identifier):
                for nb_match, one_match in enumerate(matchs['matchs_list']):
                    m = Match(one_match)    
                    if player == m.id_player_a:
                        sum_p = sum_p + m.score_player_a
                        sum_scores[str(player)] = sum_p
                        break
                    elif player == m.id_player_b:
                        sum_p = sum_p + m.score_player_b
                        sum_scores[str(player)] = sum_p
                        break
        print(sum_scores)

    def add_matchs_rd1(self, t):
        match_list = []    
        num_match = 1
        for play_1, play_2 in self.matchs_to_play_rd1(t):
            while True:
                self.matchs_to_play_rd1(t)
                num = self.input_score(num_match, play_1, play_2)
                if num:
                    break
                in_out_view.clear_console()
            match_list.append(self.match_player_score(num, play_1, play_2))
            num_match += 1
        return match_list

    def choose_to_enter_score(self, t):
        while True:
            self.matchs_to_play_rd1(t)
            choice = self.ask_enter_score()
            if choice:
                break
            in_out_view.clear_console()
        return choice
        