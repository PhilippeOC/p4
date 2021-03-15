from tinydb import TinyDB
from ..views import in_out_view
from operator import itemgetter
from ..models.tournament_manager import TournamentManager
from ..models.player_manager import PlayerManager


players_db_list = []
tournaments_db_list = []


def init_db(table_name: str):
    db = TinyDB('db.json', sort_keys=True, indent=2, separators=(',', ': '))
    table_name = db.table(table_name)
    return table_name


def write_datas_db(table_name: str, serialized_datas: dict):
    tn = init_db(table_name)
    tn.truncate()
    tn.insert_multiple(serialized_datas)


def read_datas_db(table_name: str) -> dict:
    return init_db(table_name).all()


def choose_tournament(data: list, title="Liste des tournois") -> int:
    while True:
        nb_items = in_out_view.display_tournaments(data, title)
        num = in_out_view.get_number_entry("Entrer le N° du tournoi", nb_items)
        if num:
            break
    return num


def id_player_to_player(identifier: str, data: list) -> PlayerManager:
    pm = PlayerManager()
    for num, player in enumerate(data):
        pm.create_player(player)
        play = pm.find_by_id(identifier)
        if play:
            return play


def disp_players_alpha(data: list) -> list:
    return sorted(data, key=itemgetter('lastname', 'firstname', 'ranking'))


def disp_players_rank(data: list) -> list:
    return sorted(data, key=itemgetter('ranking', 'lastname', 'firstname'))
