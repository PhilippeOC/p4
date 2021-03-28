

class Match:
    """ Retourne l'identifiant et le score des joueurs dans un match
    format des matchs:
    ([id_player_a: str, score_player_a: float], [id_player_b: str, score_player_b: float]
    """

    def __init__(self, match: tuple):
        self.__id_player_a = match[0][0]
        self.__score_player_a = match[0][1]
        self.__id_player_b = match[1][0]
        self.__score_player_b = match[1][1]

    @property
    def id_player_a(self) -> float:
        return self.__id_player_a

    @property
    def score_player_a(self) -> float:
        return self.__score_player_a

    @property
    def id_player_b(self) -> float:
        return self.__id_player_b

    @property
    def score_player_b(self) -> float:
        return self.__score_player_b
