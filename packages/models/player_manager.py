from .player import Player


class PlayerManager:
    def __init__(self):
        self.__players = {}

    #def find_all(self):
        #return self.__players

    def create_player(self, player_data: dict) -> dict:
        p = Player(**player_data)
        self.__players[str(p.identifier)] = p
        return p

    def find_by_id(self, identifier: str):
        if identifier in self.__players:
            return self.__players[identifier]
