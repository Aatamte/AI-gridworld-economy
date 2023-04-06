from src.agents.BaseAgent import BaseAgent
import random


class RandomAgent(BaseAgent):
    def __init__(self):
        super(RandomAgent, self).__init__()
        self.name = "Random Agent"

    def select_action(self, state):
        return random.choice([i for i in range(5)])