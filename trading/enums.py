from enum import Enum


class OrderType(Enum):
    BUYER = 1
    SELLER = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
