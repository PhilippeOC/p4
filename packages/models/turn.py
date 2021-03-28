from datetime import datetime


class Turn:
    """ création d'un tours
        date et heure de début et de fin du tour
    """
    def __init__(self, name: str):
        self.__name = name
        self.__match_list = []

    def create_round(self) -> dict:
        return {"name": self.__name,
                "start_datetime": self.start_datetime_round,
                "end_datetime": "tour en cours",
                "match_list": self.__match_list}

    @property
    def start_datetime_round(self) -> datetime.date:
        self.__start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.__start_datetime

    @property
    def end_datetime_round(self) -> datetime.date:
        self.__end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.__end_datetime
