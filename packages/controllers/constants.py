""" Constantes de mise en forme pour l'affichage des données """


ITEMS_PLAYERS = {"lastname": "Nom du joueur:",
                 "firstname": "Prénom du joueur:",
                 "datebirth": "Date de naissance: jour-mois-année (ex: 14-02-2000):",
                 "sex": "Genre : 1.Homme  2.Femme",
                 "ranking": "Classement:"}

ITEMS_TOURNAMENTS = {"name": "Nom du tournoi :",
                     "place": "Lieu du tournoi :",
                     "date": "Date du tournoi: jour-mois-année (ex: 14-02-2021) :",
                     "nb_turns": "Nombre de tours (4 par défaut):",
                     "time_control": "Contrôle du temps : 1.Bullet  2.Blitz  3.Coup rapide",
                     "description": "Commentaire du directeur du tournoi :"}

HEAD_PLAYERS_ALPHA = f"{'N°':^4s} {' ':1s} {'Nom':^10s} {' ':1s} {'Prémom':^10s} {' ':1s} {'Rang':^5s} {' ':2s}" \
                     f"{'Naissance':^10s} {' ':1s} {'Genre':^8s} {' ':1s} {'N° identifiant':^30s}"

HEAD_PLAYERS_RANK = f"{'N°':^4s} {' ':1s} {'Rang':^5s} {' ':2s} {'Nom':^10s} {' ':1s} {'Prémom':^10s} {' ':1s}" \
                    f"{'Naissance':^10s} {' ':1s} {'Genre':^8s} {' ':1s} {'N° identifiant':^30s}"

HEAD_TOURNAMENTS = f"{'N°':^4s} {' ':1s} {'Nom':^20s} {' ':1s} {'Lieu':^20s} {' ':1s} {'Date':^10s} {' ':1s}" \
                   f"{'Commentaire':^40s} {' ':1s}"

HEAD_TOURS = f"{'N°':^4s} {' ':1s} {'Nom':^10s} {' ':1s} {'Début':^20s} {' ':1s} {'Fin':^20s} {' ':1s}"

HEAD_MATCHS = f"{'Match':>4s} {' ':1s} {'Joueur A':^20s} {' ':1s} {'Score':^10s} {' ':1s}" \
              f"{'Joueur B':^20s} {' ':1s} {'Score':^10s}"

HEAD_MATCHS_TO_DO_RD1 = f"{'Match':>4s} {' ':1s} {'Joueur A':^20s} {' ':1s} {'Rank':^10s} {' ':1s}" \
                        f"{'Joueur B':^20s} {' ':1s} {'Rank':^10s}"

HEAD_MATCHS_TO_DO = f"{'Match':>4s} {' ':1s} {'Joueur A':^20s} {' ':1s} {'Points':^10s} {' ':1s}" \
                    f"{'Joueur B':^20s} {' ':1s} {'Points':^10s}"

HEAD_ONE_MATCH = f"{'Match':>4s} {' ':1s} {'Joueur A':^20s} {' ':1s} {'   ':^10s} {'Joueur B':^20s} {' ':1s}"
