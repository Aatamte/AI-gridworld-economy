from src.agents.BaseAgent import BaseAgent
import random


class GatheringAgent(BaseAgent):
    def __init__(self):
        super(GatheringAgent, self).__init__()
        self.name = "Random Agent"

    def select_action(self, state, prev_reward):
        if prev_reward == 0:
            return random.choice([i for i in range(5)])
        else:
            return 4