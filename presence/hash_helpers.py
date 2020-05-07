from colorhash import ColorHash


def get_username_from_ws(message):
    return ColorHash(message).hex
