from dataclasses import dataclass
import numpy as np


class COLORS:
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    ORE = "#464645"
    METAL = "#71797E"
    GREEN = "#25150B"


def default_resources():
    return {
        "wood": Resource(
            name="wood",
            a_max=40,
            id=0,
            color=COLORS.GREEN
        ),
        "ore": Resource(
            name="ore",
            a_max=20,
            id=1,
            color=COLORS.ORE
        ),
        "metals": Resource(
            name="metals",
            a_max=30,
            id=2,
            color=COLORS.METAL
        ),
        "coal": Resource(
            name="coal",
            a_max=20,
            id=3,
            color=COLORS.BLACK
        )
    }


@dataclass
class Resource:
    name: str
    a_max: int
    current_amount: int = 0
    map_dimensions: tuple = (0, 0)
    a_min: float = 0
    locations: np.ndarray = np.zeros(map_dimensions)
    color: str = None
    scarcity: str = "normal"
    id: int = None