import random

import numpy as np
import noise
import plotly.graph_objs as go
from src.env.map_objects.Resources import Resource
from src.agents.actions import ACTIONS


default_map_config = {
    "lakes": True,
    "rivers": {

    },
    "resources": None,
    "invalid_squares": None,
}


def resource_generator(x_size, y_size, num_resources, space = 0.5, seed = None):
    """
    :param map_size:
    :param num_resources:
    :return:
    """
    np.random.seed(seed)
    world = np.zeros((x_size, y_size))
    scale = 40
    octaves = 2
    persistence = 0.7
    lacunarity = 2.0
    shift_factor = np.random.randint(1, 999999)
    for i in range(x_size):
        for j in range(y_size):
            world[i][j] = noise.pnoise2(
                (i + shift_factor) / scale,
                (j + shift_factor) / scale,
                octaves,
                persistence,
                lacunarity
            )
    percentiles =[i / (num_resources) * space + (1 - space) for i in range(num_resources)]
    quintiles = np.quantile(world, percentiles)
    out = np.searchsorted(quintiles, world)
    # convert ids to quantities
    return out


def create_resource_quantities(resource_ids, resource_lookup):
    resource_quantities = np.zeros_like(resource_ids)
    for i in range(resource_quantities.shape[0]):
        for j in range(resource_quantities.shape[1]):
            if resource_ids[i, j] != 0:
                resource_quantities[i, j] = resource_lookup[resource_ids[i, j]].a_max
    return resource_quantities


class GridWorld:
    """
    Handles and stores gridworld information.

    - Procedural map creation

    """
    def __init__(
            self,
            x_size: int,
            y_size: int,
            agents: list,
            resource_parameters: dict,
            seed: int = None
    ):
        self.x_size: int = x_size
        self.y_size: int = y_size
        self.agents: list = agents
        self.resource_parameters: dict = resource_parameters
        self.num_resources: int = len(self.resource_parameters)
        self.seed: int = seed

        self.square_ids: np.ndarray = np.zeros((x_size, y_size), dtype=np.int)
        #
        self.agent_locations = np.zeros((x_size, y_size), dtype=np.int)
        self.resource_ids = np.zeros((x_size, y_size), dtype=np.int)
        self.resource_amounts = np.zeros((x_size, y_size), dtype=np.int)
        self.valid_squares = np.zeros((x_size, y_size), dtype=np.int)
        self.resource_lookup = {r.id + 1: r for r in resource_parameters.values()}
        self.resource_lookup[0] = Resource(
            name="empty",
            a_max=0
        )
        self.buildings = np.zeros((x_size, y_size))
        self.starting_resource_types = 0

        self.obstacles = True

        self.create_map(self.obstacles)
        self.changes_to_map = None

    def _initialize_resources(self):
        self.resource_ids = resource_generator(
            self.x_size,
            self.y_size,
            self.num_resources,
            seed=self.seed
        )
        self.resource_amounts = create_resource_quantities(self.resource_ids, self.resource_lookup)

    def _initialize_agents(self):
        for agent in self.agents:
            # if no starting position was specified
            if not agent.x:
                agent.x = np.random.randint(self.x_size - 1)
            if not agent.y:
                agent.y = np.random.randint(self.y_size - 1)
            self.agent_locations[agent.x][agent.y] = agent.id

    def create_map(self, obstacles):
        self._initialize_resources()
        if obstacles:
            pass

        self._initialize_agents()

    def add(self):
        raise NotImplementedError()

    def get_one_hot_coding_map(self):
        one_hot_agents = np.arange(len(self.agents)) == self.agent_locations[..., None] - 1
        one_hot_resources = np.arange(self.num_resources) == self.resource_ids[..., None] - 1
        return np.concatenate((one_hot_agents, one_hot_resources), axis=2, dtype=int)


if __name__ == '__main__':
    pass
