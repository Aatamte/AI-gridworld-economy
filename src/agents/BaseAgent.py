import numpy as np
from src.agents.actions import ACTIONS
import pickle


class BaseAgent:
    def __init__(self):
        # location information
        self.x = None
        self.y = None
        self.last_x = None
        self.last_y = None

        # for environment and rendering
        self.name = "default"
        self.color = None
        self.id = None

        # for the environment
        self.xp = 0
        self.xps = [0]
        self.inventory = {}
        self.inventory_history = []
        self.timestep = 0
        self.n_actions = None
        self.state_space = None
        self.logger = None

        # Economy
        self.current_orders = []

    def reset(self):
        del self.xps[:]
        del self.inventory_history[:]
        del self.current_orders[:]
        self.xp = 0
        self.xps = [0]
        self.inventory_history = []
        self.inventory = {"gold": 0}
        self.timestep = 0

    def get_reward(self):
        return self.xps[-1] - self.xps[-2]

    def add_inventory(self, new_inventory):
        n_inv = new_inventory.copy()
        self.xps.append(sum(n_inv.values()))
        n_inv["idx"] = self.timestep
        self.inventory_history.append(n_inv)
        self.timestep += 1

    def get_position(self):
        return self.x, self.y

    def save(self, path = None):

        if path:
            pickle.dump()
        else:
            pass
