import typing
from datetime import datetime

import pytz


moscow_tz = pytz.timezone("Europe/Moscow")


def get_datetime_msk() -> datetime:
    moscow_time = datetime.now(moscow_tz)
    return moscow_time


class TGGroup(typing.NamedTuple):
    id: str
    name: str


class DBResponse(typing.NamedTuple):
    status: str
    text: str


class ActiveTournament(typing.NamedTuple):
    id: str
    name: str
