import numpy as np
from src.agents.actions import ACTIONS


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

        # for the game
        self.xp = 0
        self.inventory = {"gold": 0}
        self.inventory_history = []
        self.totals = [0]
        self.timestep = 0
        self.action_space = []

    def reset(self):
        self.inventory_history = []
        self.inventory = {"gold": 0}
        self.totals = [0]
        self.timestep = 0

    def add_inventory(self, new_inventory):
        n_inv = new_inventory.copy()
        self.totals.append(sum(n_inv.values()))
        n_inv["idx"] = self.timestep
        self.inventory_history.append(n_inv)
        self.timestep += 1

    @staticmethod
    def get_action_type(action):
        if action == 0:
            return "move"
        elif action == 1:
            return "move"
        elif action == 2:
            return "move"
        elif action == 3:
            return "move"
        elif action == 4:
            return "gather"
        return "NA"

    def send_order(self, name, quantity, price):
        pass

    def get_position(self):
        return self.x, self.y
