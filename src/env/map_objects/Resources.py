from dataclasses import dataclass
import numpy as np


class COLORS:
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    ORE = "#464645"
    METAL = "#71797E"
    GREEN = "#25150B"
    RIVER = "#193250"


def default_resources():
    return [
        Resource(
            name="wood",
            a_max=40,
            color=COLORS.GREEN,
            scarcity=4
        ),
        Resource(
            name="ore",
            a_max=10,
            color=COLORS.ORE,
            scarcity=4,
        ),
        Resource(
            name="metal",
            a_max=5,
            color=COLORS.BLACK,
            scarcity=4
        )
    ]


@dataclass
class Resource:
    name: str
    a_max: int
    current_amount: int = 0
    color: str = None
    scarcity: float = 0.1  # percentage of map covered by the resource
    id: int = None
    regen: bool = False
    regen_rate: int = 0
    gather_amount: int = 1

    def __copy__(self):
        pass

    def copy(self):
        pass