from .tournament import Tournament


class TournamentManager:
    def __init__(self):
        self.__tournament = {}

    def create_tournament(self, tournament_data: dict) -> dict:
        t = Tournament(**tournament_data)
        self.__tournament[str(t.identifier)] = t
        return t

    """def find_rounds(self, identifier: str) -> list:
        return self.__tournament[identifier].round_list"""

    def find_matchs(self, identifier: str) -> list:
        """Retourne la liste des matchs pour chaque round """
        matchs_list = []
        round_list = self.__tournament[identifier].round_list
        if round_list:
            for num_round, items_round in enumerate(round_list):
                matchs_dict = {}
                matchs_dict['matchs_list'] = items_round['match_list']
                matchs_list.append(matchs_dict)
            return matchs_list

    """def add_player(self, identifier: str, player_id: str):
        if self.__tournament[identifier].players_id_list is None:
            self.__tournament[identifier].players_id_list = player_id
        else:
            self.__tournament[identifier].players_id_list.append(player_id)"""

    
    def find_by_id(self, identifier: str):
        pass

    def add_match(self):
        pass

    def end_tournament(self):
        pass
