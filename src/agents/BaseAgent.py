import numpy as np
from src.agents.actions import ACTIONS
import pickle
import functools


class BaseAgent:
    def __init__(self, name: str = "default"):
        # location information
        self.x = None
        self.y = None

        # for environment and rendering
        self.num_steps = 0
        self.name = name
        self.color = None
        self.id = None

        # for the environment
        self.xp = 0
        self.xps = [0]
        self.inventory = Inventory(self)
        self.action_space = ActionSpace()
        self.state_space = None
        self.logger = None

    def reset(self):
        self.num_steps = 0
        self.xp = 0

        self.xps.clear()
        self.xps = [0]
        self.inventory.reset()

    def get_reward(self):
        return self.xps[-1] - self.xps[-2]

    def get_position(self):
        return self.x, self.y

    def step(self):
        self.inventory.step()
        self.xps.append(sum(self.inventory.values()))
        self.num_steps += 1

    def save(self, path = None):
        if path:
            pickle.dump()
        else:
            pass

    @property
    def capital(self):
        return self.inventory["capital"]

    @property
    def action_space_size(self):
        return self.action_space.size


class Inventory:
    def __init__(self, agent, starting_capital: int = 0, starting_inventory: dict = None):
        self.starting_capital = starting_capital
        self.starting_inventory = starting_inventory
        self.capital = starting_capital
        self.agent = agent
        self.inventory = self.starting_inventory if self.starting_inventory  else {}
        self.history = []

    def reset(self):
        self.inventory = self.starting_inventory if self.starting_inventory  else {}
        self.capital = self.starting_capital
        self.history.clear()

    def step(self):
        self.history.append(self.inventory.copy())

    def __getitem__(self, item):
        if item in self.inventory.keys():
            return self.inventory[item]
        return 0

    def __setitem__(self, key, value):
        if key == "capital":
            self.capital = value
        elif key in self.inventory.keys():
            self.inventory[key] = value
        else:
            self.inventory[key] = value

    def values(self):
        return self.inventory.values()

    def __repr__(self):
        return \
f"""
-----------------------------
Agent: {self.agent.name} 
capital {self.capital}
{self.inventory}
-----------------------------"""


class ActionSpace:
    def __init__(self):
        self.lookup = {}
        self.total_actions = 0

    def add(self, action, action_category):
        self.lookup[self.total_actions] = action
        self.total_actions += 1

    def add_moving_actions(self):
        for action in [
            ACTIONS.MOVE_NORTH, ACTIONS.MOVE_SOUTH,
            ACTIONS.MOVE_WEST, ACTIONS.MOVE_EAST
        ]:
            self.add(action, "move")

    def add_gathering_actions(self):
        self.add(ACTIONS.GATHER, "gather")

    def add_trading_actions(self, item_name, price_step_size, quantity_step_size, max_price: int = 1000, max_quantity: int = 5):
        # add both buying and selling actions
        self.add_buying_actions(item_name, price_step_size, max_price, quantity_step_size, max_quantity)
        self.add_selling_actions(item_name, price_step_size, max_price, quantity_step_size, max_quantity)

    def add_buying_actions(self, item_name, price_step_size, quantity_step_size, max_price: int = 1000, max_quantity: int = 5):
        for quantity in range(1, max_quantity, quantity_step_size):
            for price in range(0, max_price, price_step_size):
                self.add((item_name, price, quantity), "trade")

    def add_selling_actions(self, item_name, price_step_size, quantity_step_size, max_price: int = 1000, max_quantity: int = 5):
        for quantity in range(1, max_quantity, quantity_step_size):
            for price in range(0, max_price, price_step_size):
                self.add((item_name, price, -quantity), "trade")

    def get_action_mask(self) -> np.ndarray:
        pass

    def get_valid_action(self):
        pass

    def decode(self, action):
        return self.lookup[action]

    def __repr__(self):
        return str(self.lookup)

    @property
    def size(self):
        return len(self.lookup)