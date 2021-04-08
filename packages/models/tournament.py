from . import utils
from datetime import datetime
from enum import Enum
from typing import Union


class Tournament:
    """ Modèlise un tournoi """

    class Error(Exception):
        def __init__(self, message: str):
            super().__init__(self, message)

    Time = Enum('Time', ['BULLET', 'BLITZ', 'COUP RAPIDE'])

    def __init__(self, **tournament_dict: dict):
        attr_name_error = {}
        for attr_name in ("name", "place", "date", "nb_turns", "round_list", "players_id_list",
                          "time_control", "description", "finished"):
            try:
                setattr(self, attr_name, tournament_dict[attr_name] if attr_name in tournament_dict else None)
            except Tournament.Error as err:
                attr_name_error[attr_name] = err.args[1]
        if attr_name_error:
            raise Tournament.Error(attr_name_error)

        self.__identifier = self.name + "-" + self.place + "-" + self.date.isoformat()

    def serialize(self) -> dict:
        return {"name": self.name,
                "place": self.place,
                "date": self.date.isoformat(),
                "nb_turns": self.nb_turns,
                "round_list": self.round_list,
                "players_id_list": self.players_id_list,
                "time_control": self.time_control,
                "description": self.description,
                "finished": self.finished
                }

    @property
    def identifier(self) -> str:
        return self.__identifier

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        if utils.check_name(name):
            raise Tournament.Error(f"'{name}': le nom du tournoi doit contenir au "
                                   "moins deux lettres sans ponctuation.")
        self.__name = name.upper()

    @property
    def place(self) -> str:
        return self.__place

    @place.setter
    def place(self, place: str):
        if utils.check_name(place):
            raise Tournament.Error(f"'{place}': le nom du lieu doit contenir au moins deux lettres sans ponctuation.")
        self.__place = place.capitalize()

    @property
    def date(self) -> datetime:
        return self.__date

    @date.setter
    def date(self, day: Union[str, datetime]):
        if isinstance(day, str):
            try:
                day = datetime.strptime(day, '%d-%m-%Y').date()
            except ValueError:
                try:
                    day = datetime.fromisoformat(day).date()
                except ValueError:
                    raise Tournament.Error(f"'{day}': vérifier le format de la date.")
        self.__date = day

    @property
    def nb_turns(self) -> int:
        return self.__nb_turns

    @nb_turns.setter
    def nb_turns(self, nb_turns: Union[str, int]):
        if isinstance(nb_turns, str):
            try:
                nb_turns = int(nb_turns)
            except Exception:
                raise Tournament.Error(f"'{nb_turns}': le nombre de tours est un nombre entier positif.")
        if not nb_turns > 0:
            raise Tournament.Error(f"'{nb_turns}': le nombre de tours est un nombre entier positif.")
        self.__nb_turns = nb_turns

    @property
    def round_list(self) -> list:
        return self.__round_list

    @round_list.setter
    def round_list(self, round_list: list):
        if round_list is None:
            self.__round_list = []
        else:
            self.__round_list = round_list

    @property
    def players_id_list(self) -> list:
        return self.__players_id_list

    @players_id_list.setter
    def players_id_list(self, players_id: list):
        if players_id is None:
            self.__players_id_list = []
        else:
            self.__players_id_list = players_id

    @property
    def time_control(self) -> str:
        return self.__time_control

    @time_control.setter
    def time_control(self, time_control: str):
        """ soit time_control = '1' ou '2' ou '3' ou alors time_control = 'BULLET' ou 'BLITZ' ou 'COUP RAPIDE' """
        try:
            if int(time_control) not in [item.value for item in self.Time]:
                raise Tournament.Error(f"'{time_control}': le contrôle du temps doit être:"
                                       f"1. BULLET, 2. BLITZ ou 3. COUP RAPIDE")
            for item in self.Time:
                if int(time_control) == item.value:
                    self.__time_control = item.name
                    break
        except ValueError:
            if time_control not in [item.name for item in self.Time]:
                raise Tournament.Error(f"'{time_control}': le contrôle du temps doit être:"
                                       f"1. BULLET, 2. BLITZ ou 3. COUP RAPIDE")
            for item in self.Time:
                if time_control == item.name:
                    self.__time_control = item.name
                    break

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        self.__description = description

    @property
    def finished(self) -> str:
        return self.__finished

    @finished.setter
    def finished(self, finished: bool):
        self.__finished = finished
