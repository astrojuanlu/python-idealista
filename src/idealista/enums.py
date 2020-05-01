from enum import Enum


class PropertyType(Enum):
    HOMES = "homes"
    OFFICES = "offices"
    PREMISES = "premises"
    GARAGES = "garages"
    BEDROOMS = "bedrooms"


class Operation(Enum):
    RENT = "rent"
    SALE = "sale"


class SinceDate(Enum):
    LAST_WEEK = "W"
    LAST_MONTH = "M"
    LAST_DAY = "T"
    LAST_TWO_DAYS = "Y"


class Sort(Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"
