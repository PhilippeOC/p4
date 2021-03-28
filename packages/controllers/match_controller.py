
from .import utils
from ..views import in_out_view
from ..models.tournament_manager import TournamentManager
from ..models.player_manager import PlayerManager
from ..models.match import Match
from operator import itemgetter
from ..models.turn import Turn


class MatchController:
    """ Gestion des matchs: scores et joueurs
        matchmaking
    """
    def __init__(self):
        self.tm = TournamentManager()
        self.pm = PlayerManager()
        self.data_t = utils.tournaments_db_list
        self.data_p = utils.players_db_list

    def matchs_to_play_rd1(self, tournament: TournamentManager) -> list:
        """ retourne la liste des matchs à jouer du round 1 """
        play_by_rank = self.player_by_rank(tournament)
        value = len(play_by_rank) // 2
        lower_list = play_by_rank[0:value]
        upper_list = play_by_rank[value: len(play_by_rank)]
        matchs_to_play = []
        for num, player in enumerate(lower_list):
            matchs_to_play.append((lower_list[num], upper_list[num]))
        in_out_view.disp_matchs_to_do(matchs_to_play, "Round 1")
        return matchs_to_play

    def player_by_rank(self, tournament: TournamentManager):
        """ retourne la liste des joueurs du round 1 classés par rank croissant:
            ranking, lastname, firstname """
        play_data_list = []
        for id_players in tournament.players_id_list:
            play_data = {}
            play_data['ranking'] = utils.id_player_to_player(id_players, self.data_p).ranking
            play_data['lastname'] = utils.id_player_to_player(id_players, self.data_p).lastname
            play_data['firstname'] = utils.id_player_to_player(id_players, self.data_p).firstname
            play_data['identifier'] = str(utils.id_player_to_player(id_players, self.data_p).identifier)
            play_data_list.append(play_data)
        return utils.disp_players_rank(play_data_list)

    def choose_to_enter_score(self, tournament: dict, round_name: str) -> int:
        if round_name == 'Round 1':
            while True:
                self.matchs_to_play_rd1(tournament)
                choice = self.ask_enter_score()
                if choice:
                    break
                in_out_view.clear_console()
            return choice
        else:
            while True:
                in_out_view.disp_matchs_to_do(self.next_matchs_to_play(tournament), round_name)
                choice = self.ask_enter_score()
                if choice:
                    break
                in_out_view.clear_console()
            return choice

    def ask_enter_score(self) -> int:
        in_out_view.disp_ask_enter_score()
        return in_out_view.get_number_entry("Votre choix", 2)

    def input_score(self, num_match: int, play_1: dict, play_2: dict):
        in_out_view.display_title("Entrer les scores des matchs", False)
        in_out_view.disp_one_match(num_match, play_1, play_2)
        in_out_view.to_enter_the_scores()
        return in_out_view.get_number_entry("Entrer le résultat du match", 2)

    def match_player_score(self, num: int, play_1: dict, play_2: dict) -> tuple:
        winner = 1
        loser = 0
        tie_game = 0.5
        if num == 1:
            return ([play_1['identifier'], winner], [play_2['identifier'], loser])
        elif num == 2:
            return ([play_1['identifier'], loser], [play_2['identifier'], winner])
        elif num == 3:
            return ([play_1['identifier'], tie_game], [play_2['identifier'], tie_game])

    def sum_of_scores(self, tournament: TournamentManager) -> dict:
        """ retourne un dict {'id du player': somme de ses scores} """
        self.tm.create_tournament(tournament.serialize())
        sum_scores = {}
        for num, player in enumerate(tournament.players_id_list):
            sum_p = 0
            for matchs in self.tm.find_matchs(tournament.identifier):
                for one_match in matchs['matchs_list']:
                    m = Match(one_match)
                    if player == m.id_player_a:
                        sum_p = sum_p + m.score_player_a
                        sum_scores[str(player)] = sum_p
                        break
                    elif player == m.id_player_b:
                        sum_p = sum_p + m.score_player_b
                        sum_scores[str(player)] = sum_p
                        break
        return sum_scores

    def players_by_scores(self, scores_data: dict) -> list:
        data = []
        for id_player, score in scores_data.items():
            player_data = {}
            player_data['lastname'] = utils.id_player_to_player(id_player, self.data_p).lastname
            player_data['firstname'] = utils.id_player_to_player(id_player, self.data_p).firstname
            player_data['ranking'] = utils.id_player_to_player(id_player, self.data_p).ranking
            player_data['score'] = score
            player_data['identifier'] = str(utils.id_player_to_player(id_player, self.data_p).identifier)
            data.append(player_data)
        data = sorted(data, key=itemgetter('score', 'ranking', 'lastname', 'firstname'), reverse=False)
        return data

    def add_matchs_in_round(self, tournament: TournamentManager, round_name: str) -> list:
        match_list = []
        num_match = 1
        if round_name == 'Round 1':
            for play_1, play_2 in self.matchs_to_play_rd1(tournament):
                while True:
                    self.matchs_to_play_rd1(tournament)
                    num = self.input_score(num_match, play_1, play_2)
                    if num:
                        break
                    in_out_view.clear_console()
                match_list.append(self.match_player_score(num, play_1, play_2))
                num_match += 1
        else:
            for play_1, play_2 in self.next_matchs_to_play(tournament):
                while True:
                    in_out_view.disp_matchs_to_do(self.next_matchs_to_play(tournament), round_name)
                    num = self.input_score(num_match, play_1, play_2)
                    if num:
                        break
                    in_out_view.clear_console()
                match_list.append(self.match_player_score(num, play_1, play_2))
                num_match += 1
        return match_list

    def already_played_with(self, tournament: TournamentManager, play_a, play_b) -> bool:
        """ retourne True si les 2 joueurs ont déjà joué ensemble """
        self.tm.create_tournament(tournament.serialize())
        for matchs in self.tm.find_matchs(tournament.identifier):
            for one_match in matchs['matchs_list']:
                m = Match(one_match)
                if play_a == m.id_player_a and play_b == m.id_player_b:
                    return True
                if play_a == m.id_player_b and play_b == m.id_player_a:
                    return True

    def player_already_in_a_match(self, matchs_list: list, player: str) -> bool:
        """ retourne True si le joueur est déjà dans un match"""
        for num, play in enumerate(matchs_list):
            if player == play[0]['identifier']:
                return True
            elif player == play[1]['identifier']:
                return True

    def match_making_first_round(self, tournament: TournamentManager):
        match_to_disp = []
        self.create_round("Round 1", tournament)
        if self.choose_to_enter_score(tournament, "Round 1") == 2:
            return True
        tournament.round_list[0]['match_list'] = self.add_matchs_in_round(tournament, "Round 1")
        match_to_disp.append(utils.match_player_score(tournament.round_list[0]['match_list']))
        in_out_view.display_matchs(match_to_disp, "Round 1", f"Tournoi: {tournament.name} à {tournament.place} "
                                                             f"le {tournament.date}")

    def match_making_other_rounds(self, tournament: TournamentManager, num_round: str):
        match_to_disp = []
        round_name = "Round " + str(num_round)
        in_out_view.disp_matchs_to_do(self.next_matchs_to_play(tournament), round_name)
        if self.choose_to_enter_score(tournament, round_name) == 2:
            return True
        self.create_round(round_name, tournament)
        tournament.round_list[num_round-1]['match_list'] = self.add_matchs_in_round(tournament, round_name)
        match_to_disp.append(utils.match_player_score(tournament.round_list[num_round-1]['match_list']))
        in_out_view.display_matchs(match_to_disp, round_name, f"Tournoi: {tournament.name} à {tournament.place} "
                                                              f"le {tournament.date}")

    def next_matchs_to_play(self, tournament: TournamentManager) -> list:
        """retourne la liste des prochains matchs à jouer matchmaking"""
        players_scores = self.players_by_scores(self.sum_of_scores(tournament))
        nb_match = 1
        num_player_a = 0
        num_player_b = 1
        not_erase = False
        next_matchs = []
        while nb_match <= len(players_scores)/2:
            play_a = players_scores[num_player_a]
            if self.player_already_in_a_match(next_matchs, play_a['identifier']):
                num_player_a += 1
                num_player_b += 1
                continue
            while True:
                if num_player_b < len(players_scores):
                    play_b = players_scores[num_player_b]
                    if self.player_already_in_a_match(next_matchs, play_b['identifier']):
                        num_player_b += 1
                        continue
                    if self.already_played_with(tournament, play_a['identifier'], play_b['identifier']):
                        num_player_b += 1
                        continue
                    else:
                        next_matchs.append((play_a, play_b))
                        num_player_b += 1
                        num_player_a += 1
                        nb_match += 1
                        break
                else:
                    overflow = num_player_b-len(players_scores)
                    play_b = players_scores[overflow]
                    if overflow == 0:
                        if not not_erase:
                            next_matchs[overflow] = (play_a, play_b)
                            not_erase = True
                            num_player_a += 1
                            num_player_b = num_player_a + 1
                        else:
                            num_player_b += 1
                    else:
                        next_matchs.append((play_a, play_b))
                        nb_match += 1
                    break
        return next_matchs

    def create_round(self, name: str, tournament: TournamentManager):
        rd = {}
        self.rd = Turn(name)
        rd['name'] = name
        tournament.round_list.append(self.rd.create_round())

    def end_round(self, tournament: TournamentManager, num_round: int):
        name = "Round " + str(num_round)
        self.rd = Turn(name)
        tournament.round_list[num_round-1]['end_datetime'] = self.rd.end_datetime_round
