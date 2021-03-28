from . import utils
from datetime import datetime
from enum import Enum
from typing import Union
import uuid


class Player:
    """ Modèlise un joueur """

    class Error(Exception):
        def __init__(self, message: str):
            super().__init__(self, message)

    Gender = Enum("Gender", "Homme Femme")

    def __init__(self, **player_dict: dict):
        attr_name_error = {}
        for attr_name in ("identifier", "lastname", "firstname", "sex", "datebirth", "ranking"):
            try:
                setattr(self, attr_name, player_dict[attr_name] if attr_name in player_dict else None)
            except Player.Error as err:
                attr_name_error[attr_name] = err.args[1]
        if attr_name_error:
            raise Player.Error(attr_name_error)

    def serialize(self) -> dict:
        return {"lastname": self.lastname,
                "firstname": self.firstname,
                "datebirth": self.datebirth.isoformat(),
                "sex": self.sex,
                "ranking": self.ranking,
                "identifier": str(self.identifier)
                }

    @property
    def identifier(self) -> uuid.UUID:
        return self.__identifier

    @identifier.setter
    def identifier(self, value: Union[uuid.UUID, str]):
        if value is None:
            self.__identifier = uuid.uuid4()
        elif isinstance(value, str):
            try:
                value = uuid.UUID(value)
            except Player.Error:
                raise Player.Error("L'attribution d'un identifiant a échoué")
            self.__identifier = value
        elif isinstance(value, uuid.UUID):
            if value.version != 4:
                raise Player.Error("La version du numéro de l'identifiant n'est pas correcte")
            self.__identifier = value

    @property
    def lastname(self) -> str:
        return self.__lastname

    @lastname.setter
    def lastname(self, last_name: str):
        if utils.check_name(last_name):
            raise Player.Error(f"'{last_name}': Le nom doit contenir au moins deux lettres sans ponctuation.")
        self.__lastname = last_name.upper()

    @property
    def firstname(self) -> str:
        return self.__firstname

    @firstname.setter
    def firstname(self, first_name: str):
        if utils.check_name(first_name):
            raise Player.Error(f"'{first_name}': Le prénom doit contenir au moins deux lettres sans ponctuation.")
        self.__firstname = first_name.capitalize()

    @property
    def datebirth(self) -> datetime:
        return self.__datebirth

    @datebirth.setter
    def datebirth(self, born: Union[str, datetime]):
        age_min = 18
        age_max = 100
        if isinstance(born, str):
            try:
                born = datetime.strptime(born, '%d-%m-%Y').date()
            except ValueError:
                try:
                    born = datetime.fromisoformat(born).date()
                except ValueError:
                    raise Player.Error(f"'{born}': vérifier le format de la date.")
        dt = datetime.today()
        age = dt.year - born.year - ((dt.month, dt.day) < (born.month, born.day))
        if not age_min < age < age_max:
            raise Player.Error(f"'{age}' ans: vous devez avoir entre {age_min} et {age_max} ans pour participer.")
        self.__datebirth = born

    @property
    def sex(self) -> str:
        return self.__sex

    @sex.setter
    def sex(self, sex: str):
        # soit sex = '1' ou '2' ou alors sex = 'Homme' ou 'Femme'
        try:
            if int(sex) not in [item.value for item in self.Gender]:
                raise Player.Error(f"'{sex}': impossible, saisir 1 pour Homme ou 2 pour Femme.")
            for item in self.Gender:
                if int(sex) == item.value:
                    self.__sex = item.name
                    break
        except ValueError:
            if sex not in [item.name for item in self.Gender]:
                raise Player.Error(f"'{sex}': impossible, saisir 1 pour Homme ou 2 pour Femme.")
            for item in self.Gender:
                if sex == item.name:
                    self.__sex = item.name
                    break

    @property
    def ranking(self) -> int:
        return self.__ranking

    @ranking.setter
    def ranking(self, rank: str):
        rank_min = 0
        rank_max = 3000
        rank = int(rank)
        if not rank_min <= rank <= rank_max:
            raise Player.Error(f"'{rank}': le classement est un nombre compris entre {rank_min} et {rank_max}.")
        self.__ranking = rank
