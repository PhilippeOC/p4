import re


def check_name(name: str):
    """ retourne false si name contient des caractères de ponctuation,
    des chiffres ou des caractères spéciaux ou un seul caractère"""
    return re.match(r"^[A-Za-z '-'\éèêëàâîïùûüôÿçÉÈÊËÀÂÏÎÙÛÜÔŸÇ']{2,}$", name) is None
