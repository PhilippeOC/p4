from .import utils
from .import constants
from .import menus_controller
from ..models.player import Player
#from ..views import in_out_view

from ..models.player_manager import PlayerManager
from ..views.in_out_view import get_user_entry


class PlayerController:
    def __init__(self, item):
        self.item = item
        self.pm = PlayerManager()
        self.data_p = utils.players_db_list
        self.title = ""

    def run(self):
        if self.item == 'add new players':
            self.title = "Ajout d'un nouveau joueur"
            self.data_p.append(self.add_player())
            return menus_controller.player_add_menu()

    def add_player(self):
        player_data = {}
        for key, data in constants.ITEMS_PLAYERS.items():
            player_data[key] = get_user_entry(self.title, "", data, None)
        return self.create_player(player_data)

    def create_player(self, player_data: dict):
        try:
            p = self.pm.create_player(player_data)
            return p.serialize()
        except Player.Error as err:
            return self.error_entries(player_data, err.args[1])

    def error_entries(self, player_data: dict, errors: dict):
        for item_key, message in errors.items():
            ask = constants.ITEMS_PLAYERS[item_key]
            player_data[str(item_key)] = get_user_entry(self.title, message, ask, None)
        return self.create_player(player_data)
