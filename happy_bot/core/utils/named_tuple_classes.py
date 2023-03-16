"""NAMED TUPLE CLASSES FOR DISPLAYING INFORMATION"""
from typing import NamedTuple
from datetime import datetime, date


class RInfo(NamedTuple):
    """
    Information about reminders
    """
    id: int
    title: str
    birth_date: date
    age: int
    text: str
    rem_time: datetime


class BDinfo(NamedTuple):
    """
    Information about birthdays
    """
    id: int
    title: str
    content: str
    photo_path: str
    birth_date: date
    age: int
