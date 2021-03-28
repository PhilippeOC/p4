from .tournament import Tournament


class TournamentManager:
    """ Création d'un tournoi
        Liste des matchs présents dans un tournoi
    """
    def __init__(self):
        self.__tournament = {}

    def create_tournament(self, tournament_data: dict) -> dict:
        t = Tournament(**tournament_data)
        self.__tournament[str(t.identifier)] = t
        return t

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
