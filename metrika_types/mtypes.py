from dataclasses import dataclass
from datetime import date, time


@dataclass
class Entry:

    day: date
    id: int


@dataclass
class DayEntry:

    id: int
    date_val: date


@dataclass
class FoodEntry(Entry):

    food_type: str
    meal_count: int
    calories: float
    description: str


@dataclass
class RatingEntry(Entry):

    rating_type: str
    rating: float


@dataclass
class TimeEntry(Entry):

    event_time: time


@dataclass
class WeightEntry(Entry):

    weight: int
