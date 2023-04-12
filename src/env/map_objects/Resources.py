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
    return {
        "wood": Resource(
            name="wood",
            a_max=40,
            id=0,
            color=COLORS.GREEN
        )
    }


@dataclass
class Resource:
    name: str
    a_max: int
    current_amount: int = 0
    color: str = None
    scarcity: int = 5
    id: int = None