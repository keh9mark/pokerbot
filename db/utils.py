import typing
from datetime import datetime

import pytz


moscow_tz = pytz.timezone("Europe/Moscow")


def get_datetime_msk() -> str:
    moscow_time = datetime.now(moscow_tz)
    return moscow_time.strftime("%d.%m.%Y %H:%M:%S")


class TGGroup(typing.NamedTuple):
    id: str


class DBResponse(typing.NamedTuple):
    status: str
    text: str
