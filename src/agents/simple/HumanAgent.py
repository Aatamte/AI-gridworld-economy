from src.agents.BaseAgent import BaseAgent
from msvcrt import getche
import sys
import numpy as np
import random


class HumanAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.name = "human"

    def select_action(self):
        print(f"agent ({self.color}) {self.name}'s move: ")
        key = int(getche().decode())
        if key == 8:
            return 0
        elif key == 2:
            return 1
        elif key == 4:
            return 2
        elif key == 6:
            return 3
        else:
            return int(key)

    def random_action(self):
        return random.choice([8, 4, 2 ,6 ,5])