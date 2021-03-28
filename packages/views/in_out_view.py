import os
import sys
from ..controllers import constants
from typing import Union

""" Fonctions d'affichage et de saisie de donneés utilisées dans les modules du package views """


def clear_console():
    os.system('cls') if sys.platform.startswith('win32') else os.system('clear')


def title(title: str):
    print()
    print("****** " + title + " ******")
    print()


def subtitle(subtitle: str, clear=False):
    if clear:
        clear_console()
    print(subtitle)
    print()


def display_title(the_title: str, clear=True):
    if clear:
        clear_console()
    title(the_title)


def display_players_aplhabetic(data: list,  clear=True):
    display_title("Liste des joueurs par ordre alphabétique", clear)
    print(constants.HEAD_PLAYERS_ALPHA)
    for num, item in enumerate(data):
        data = f"{str(num+1):>4s} {' ':1s} {item['lastname']:<10} {' ':1s} {item['firstname']:<10s} {' ':1s}" \
               f"{item['ranking']:>5d} {' ':2s} {item['datebirth']:>10s} {' ':1s} {item['sex']:^8s} {' ':1s}" \
               f"{item['identifier']:^30s}"
        print(data)
    return num


def disp_players_aplhabetic(data: list,  clear=True):
    for num, item in enumerate(data):
        data = f"{item[0]:<10} {' ':1s} {item[1]:<10s} {' ':1s}"
        print(data)
    return num


def display_players_less8(data: list, sub_title="par défaut", title="Liste des joueurs du tournoi"):
    display_title(title, clear=True)
    subtitle(sub_title)
    disp_players_aplhabetic(data,  clear=False)


def display_players_rank(data: list, clear=True):
    display_title("Liste des joueurs par classement", clear)
    print(constants.HEAD_PLAYERS_RANK)
    for num, item in enumerate(data):
        data = f"{str(num + 1):>4s} {' ':1s} {item['ranking']:>5d} {' ':2s} {item['lastname']:<10s} {' ':1s}" \
               f"{item['firstname']:<10s} {' ':1s} {item['datebirth']:^10s} {' ':1s} {item['sex']:^8s}"\
               f"{' ':1s} {item['identifier']:^30s}"
        print(data)
    return num


def display_tournaments(data: list, title="Liste des tournois"):
    display_title(title)
    print(constants.HEAD_TOURNAMENTS)
    for num, item in enumerate(data):
        data = f"{str(num + 1):>4s} {' ':1s} {item['name']:<20s} {' ':1s} {item['place']:<20} {' ':1s}" \
               f"{item['date']:^20s} {' ':1s} {item['description']:<40s} {' ':1s}"
        print(data)
    return num


def display_players_in_tournaments(data: tuple, sub_title: str):
    clear_console()
    display_title("Liste des joueurs d'un tournois", clear=False)
    subtitle(sub_title)
    display_players_aplhabetic(data[0],  clear=False)
    display_players_rank(data[1],  clear=False)


def display_tours(data: list, sub_title: str):
    display_title("Liste des tours")
    subtitle(sub_title)
    print(constants.HEAD_TOURS)
    for num, item in enumerate(data):
        data = f"{str(num + 1):>4s} {' ':1s} {item['name']:^10s} {' ':1s} {item['start_datetime']:^20} {' ':1s}" \
               f" {item['end_datetime']:^20s} {' ':1s}"
        print(data)
    return num


def display_matchs(data: list, round_name: str, sub_title: str):
    display_title("Liste des matchs")
    subtitle(sub_title)
    for num_round, matchs in list(enumerate(data)):
        if round_name is None:
            print("Round " + str(num_round+1))
        else:
            print(round_name)
        print(constants.HEAD_MATCHS)
        for num, item in matchs.items():
            data = f"{num:>4s} {' ':1s} {item[0][0][0]:<10s} {' ':1s} {item[0][0][1]:<10s} {' ':1s} {item[0][1]:<6}"\
                   f"{'-- ':^4s} {item[1][0][0]:<10s} {' ':1s} {item[1][0][1]:<10s} {item[1][1]:<6}"
            print(data)


def disp_matchs_to_do(data: list, sub_title: str):
    display_title("Liste des matchs à jouer")
    subtitle(sub_title)
    if sub_title == 'Round 1':
        print(constants.HEAD_MATCHS_TO_DO_RD1)
        for num, matchs in enumerate(data):
            disp_data = f"{str(num + 1):>4s} {' ':1s} {matchs[0]['lastname']:<10s} {' ':1s}"\
                        f"{matchs[0]['firstname']:<10s} {' ':1s} {matchs[0]['ranking']:<6} {'-- ':^4s}"\
                        f"{matchs[1]['lastname']:<10s} {' ':1s} {matchs[1]['firstname']:<10s}"\
                        f"{matchs[1]['ranking']:<6}"
            print(disp_data)
        print()
    else:
        print(constants.HEAD_MATCHS_TO_DO)
        for num, matchs in enumerate(data):
            disp_data = f"{str(num + 1):>4s} {' ':1s} {matchs[0]['lastname']:<10s} {' ':1s}"\
                        f"{matchs[0]['firstname']:<10s} {' ':1s} {matchs[0]['score']:<6} {'-- ':^4s}"\
                        f"{matchs[1]['lastname']:<10s} {' ':1s} {matchs[1]['firstname']:<10s}"\
                        f"{matchs[1]['score']:<6}"
            print(disp_data)
        print()


def disp_one_match(num_match: int, play_1: dict, play_2: dict):
    print(constants.HEAD_ONE_MATCH)
    data = f"{str(num_match):>4s} {' ':1s} {play_1['lastname']:<10s} {' ':1s} {play_1['firstname']:<10s} {' ':1s}"\
           f" {'-- ':^10s} {play_2['lastname']:<10s} {' ':1s} {play_2['firstname']:<10s}"
    print(data)


def disp_ask_enter_score():
    print()
    print()
    print("1. Entrer les scores des matchs")
    print("2. Menu précédent")


def to_enter_the_scores():
    print()
    print()
    print("1. Le joueur A a gagné")
    print("2. Le joueur B a gagné")
    print("3. Le match est nul")


def get_user_entry(title: str, msg: str, ask_for: str, default_value: str) -> str:
    display_title(title)
    print(msg)
    usr_entry = input(ask_for + " >> ").strip()
    while not usr_entry:
        if default_value:
            usr_entry = default_value
        else:
            display_title(title)
            print(msg)
            usr_entry = input(ask_for + " >> ").strip()
    return usr_entry


def wait():
    print()
    os.system("pause")


def come_back(message="") -> bool:
    print()
    print(message)
    choice = input("Taper 'q' pour revenir au menu précédent: >> ")
    if choice == 'q':
        return True


def get_number_entry(ask_for: str, nb_items: int) -> Union[int, bool]:
    print()
    try:
        choice = input(ask_for + " >> ").strip()
        if int(choice) in list(range(1, nb_items + 2)):
            return int(choice)
    except ValueError:
        return False
