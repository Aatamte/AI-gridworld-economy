from src.agents.BaseAgent import BaseAgent
import random


class GatheringAgent(BaseAgent):
    def __init__(self):
        super(GatheringAgent, self).__init__()
        self.name = "Random Gathering Agent"

    def select_action(self, state):
        if self.timestep >= 1:
            prev_reward = self.get_reward()
            if prev_reward == 0:
                return random.choice([i for i in range(self.n_actions)])
            else:
                return 4
        else:
            return random.choice([i for i in range(self.n_actions)])