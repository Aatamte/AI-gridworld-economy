from dataclasses import dataclass
import numpy as np
from src.env.Visualizer import Colors


def default_resources():
    return {
        "wood": Resource(
            name="wood",
            a_max=40,
            id=0,
            color=Colors.GREEN
        ),
        "ore": Resource(
            name="ore",
            a_max=20,
            id=1,
            color=Colors.ORE
        ),
        "metals": Resource(
            name="metals",
            a_max=30,
            id=2,
            color=Colors.METAL
        ),
        "coal": Resource(
            name="coal",
            a_max=20,
            id=3,
            color=Colors.BLACK
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
    color: tuple = None
    scarcity: str = "normal"
    id: int = None