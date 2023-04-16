import dataclasses
import numpy as np
import noise
from src.env.map_objects.Resources import Resource
import math
from copy import deepcopy


class Grid:
    """
    A class that represents a 2 dimensional list of Blocks
    """
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.data = [[Block(
            x=_x,
            y=_y,
            agent_here=False,
            contains=None,
            invalid_agent_block=False
        ) for _x in range(self.x)] for _y in range(self.y)]

        self.resource_key = np.zeros((self.x, self.y))

    def __getitem__(self, tup):
        return self.data[tup[0]][tup[1]]

    @property
    def to_one_hot(self):
        return 1

    @property
    def shape(self):
        return self.x, self.y

    @property
    def size(self):
        return self.x * self.y

    def reset(self):
        for i in range(self.x):
            for j in range(self.y):
                if self.data[i][j].contains:
                    self.data[i][j].contains = None
                    self.data[i][j].invalid_agent_block = False
                    self.data[i][j].agent_here = False
                    self.resource_key[i][j] = 0

    def create_blotch(self, resource: Resource, blotch_size):
        resource_count = resource.scarcity
        resource.current_amount = resource.a_max
        for blotch in range(math.ceil(resource_count / blotch_size)):
            x_cord = np.random.randint(1, self.x - 1)
            y_cord = np.random.randint(1, self.y - 1)
            self.data[x_cord][y_cord].contains = deepcopy(resource)
            self.resource_key[x_cord][y_cord] = resource.id

            self.data[x_cord - 1][y_cord].contains = deepcopy(resource)
            self.resource_key[x_cord - 1][y_cord] = resource.id

            self.data[x_cord - 1][y_cord + 1].contains = deepcopy(resource)
            self.resource_key[x_cord - 1][y_cord + 1] = resource.id

            self.data[x_cord][y_cord + 1].contains = deepcopy(resource)
            self.resource_key[x_cord][y_cord + 1] = resource.id

            resource_count -= blotch_size


@dataclasses.dataclass
class Block:
    x: int
    y: int
    agent_here: bool
    contains: object
    invalid_agent_block: bool


class GridWorld:
    """
    A class to represent the "physical" gridworld
    ...
    Attributes
    ------------------------

    """
    def __init__(
            self,
            x_size: int,
            y_size: int,
            agents: list,
            resources: list,
            seed: int = None
    ):
        """

        """
        self.x_size: int = x_size
        self.y_size: int = y_size
        self.agents: list = agents
        self.seed: int = seed
        self.episode = None
        self.curr_step = 0

        # array of gridworld size where no agent here -> 0,
        # agent is here -> agent.id
        self.agent_locations = np.zeros((x_size, y_size), dtype=np.int8)

        self.grid = Grid(self.x_size, self.y_size)
        ### RESOURCES ###
        self.resource_placement = "automatic"
        self.resources: list = resources
        self.num_resources: int = len(self.resources)
        self.hex_codes = {0: "#8A9A5B"}

        # TODO: could combine resource_ids and amounts into one three dim array
        self.resource_amounts = np.zeros((x_size, y_size), dtype=np.int8)

    def _init_resources(self, normalize_scarcity_factor: float = 1.0):
        """

        """
        blotch_size = 4
        resource_scarcity_sum = 0
        self.resource_block_count = {}
        idx = 1
        for resource in self.resources:
            if isinstance(resource.scarcity, int):
                resource_scarcity_sum += resource.scarcity / self.size
                self.resource_block_count[resource.name] = resource.scarcity
            elif isinstance(resource.scarcity, float):
                resource_scarcity_sum += resource.scarcity
                resource.scarcity *= self.size
                self.resource_block_count[resource.name] = resource.scarcity
            else:
                raise TypeError(f"Resource scarcity must be int or float, not {type(resource.scarcity)}")

            resource.id = idx
            self.hex_codes[idx] = resource.color
            # add resource to GridWorld
            self.grid.create_blotch(resource, blotch_size)
            idx += 1

        # check scarcity factors
        # user could define scarcities that sum to be > 1
        if resource_scarcity_sum > 1:
            raise Warning("Resource scarcity factors sum to be greater than 1 (total number of resources in the GridWorld is greater than the size of GridWorld)")

    def add(self):
        raise NotImplementedError()

    def reset(self):
        self.curr_step = 0
        if self.episode:
            self.episode += 1
        else:
            self.episode = 0

        self.grid.reset()
        self._init_resources()
        for agent in self.agents:
            # if no starting position was specified
            if not agent.x:
                agent.x = np.random.randint(self.x_size - 1)
            if not agent.y:
                agent.y = np.random.randint(self.y_size - 1)
            self.agent_locations[agent.x][agent.y] = agent.id
            self.grid[agent.x, agent.y].agent_here = True

    def step(self):
        self.curr_step += 1

    def get_one_hot_coding_map(self):
        one_hot_agents = np.arange(len(self.agents)) == self.agent_locations[..., None] - 1
        one_hot_resources = np.arange(self.num_resources) == self.resource_ids[..., None] - 1
        return np.concatenate((one_hot_agents, one_hot_resources), axis=2, dtype=int)

    def __getitem__(self, tup):
        return self.grid[tup[0], tup[1]]

    @property
    def get_resource_locations(self):
        return self.grid.resource_key.tolist()

    @property
    def size(self):
        return self.grid.size


if __name__ == '__main__':
    grid = Grid(10, 15)

    print(grid[9, 4])
