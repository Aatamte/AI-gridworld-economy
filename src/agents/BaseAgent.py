import numpy as np


class ACTIONS:
    MOVE_NORTH = 8
    MOVE_SOUTH = 2
    MOVE_WEST = 4
    MOVE_EAST = 6
    GATHER = 5


class BaseAgent:
    def __init__(self):
        self.x = None
        self.y = None
        self.grid = None
        self.last_x = None
        self.last_y = None
        self.bounds = None
        self.name = "default"
        self.color = None
        self.id = None
        self.inventory = {}
        self.inventory_history = []
        self.timestep = 0

    def reset(self, grid):
        pass

    def add_inventory(self, new_inventory):
        n_inv = new_inventory.copy()
        n_inv["idx"] = self.timestep
        self.inventory_history.append(
            n_inv
        )
        self.timestep += 1

    def move_north(self):
        self.y -= 1

    def move_south(self):
        self.y += 1

    def move_west(self):
        self.x -= 1

    def move_east(self):
        self.x += 1

    def check_bounds(self):
        if self.x > self.bounds:
            self.x = self.bounds
        elif self.x < 0:
            self.x = 0
        if self.y > self.bounds:
            self.y = self.bounds
        elif self.y < 0:
            self.y = 0

    @staticmethod
    def get_action_type(action):
        if action == 8:
            return "move"
        elif action == 2:
            return "move"
        elif action == 6:
            return "move"
        elif action == 4:
            return "move"
        elif action == 5:
            return "gather"
        return "NA"

    def handle_action(self, action):
        self.last_y = self.y
        self.last_x = self.x
        if action == 8:
            self.move_north()
        elif action == 2:
            self.move_south()
        elif action == 6:
            self.move_east()
        elif action == 4:
            self.move_west()
        else:
            return False
        self.check_bounds()
        return True