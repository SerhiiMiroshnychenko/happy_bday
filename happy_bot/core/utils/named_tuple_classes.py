from typing import NamedTuple

from datetime import datetime, date


class Info(NamedTuple):
    id: int
    title: str
    birth_date: date
    age: int
    text: str
    rem_time: datetime


class BDinfo(NamedTuple):
    id: int
    title: str
    content: str
    photo_path: str
    birth_date: date
    age: int
