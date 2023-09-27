from datetime import datetime


def get_now_int():
    return int(datetime.now().timestamp())


QUALITY_DIACRITIC_LOOKUP = {"long": "ː"}
