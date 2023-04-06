from src.agents.BaseAgent import BaseAgent
from msvcrt import getche
import sys
import numpy as np
import random


class HumanAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.name = "human"
        self.x = None
        self.y = None

    def select_action(self):
        print(f"agent ({self.color}) {self.name}'s move: ")
        key = getche().decode()
        return int(key)

    def random_action(self):
        return random.choice([8, 4, 2 ,6 ,5])