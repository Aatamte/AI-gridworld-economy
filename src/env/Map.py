import random

import numpy as np
import noise
import plotly.graph_objs as go
from src.env.Resources import Resource


class Block:
    def __init__(self):
        pass


def resource_generator(map_size, num_resources, space = 0.2, seed = None):
    """
    :param map_size:
    :param num_resources:
    :return:
    """
    np.random.seed(seed)
    world = np.zeros((map_size, map_size))
    scale = 100
    octaves = 3
    persistence = 0.7
    lacunarity = 3.0
    shift_factor = np.random.randint(1, 999999)
    for i in range(map_size):
        for j in range(map_size):
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


class Map:
    def __init__(
            self,
            n,
            agents,
            resource_parameters,
            seed=None
    ):
        self.n = n
        self.agents = agents
        self.resource_parameters = resource_parameters
        self.num_resources = len(self.resource_parameters)
        self.seed = seed
        self.grid = np.zeros((n, n), dtype=np.int)
        self.agent_locations = np.zeros((n, n), dtype=np.int)
        self.resource_ids = np.zeros((n, n), dtype=np.int)
        self.resource_amounts = np.zeros((n, n), dtype=np.int)
        self.valid_squares = np.zeros((n, n), dtype=np.int)
        self.resource_lookup = {r.id + 1: r for r in resource_parameters.values()}
        self.resource_lookup[0] = Resource(
            name="empty",
            a_max=0
        )
        self.buildings = np.zeros((n, n))
        self.starting_resource_types = 0

        self.obstacles = True

        self.create_map(self.obstacles)

    def describe(self):
        print("""
        """)

    def _initialize_resources(self):
        self.resource_ids = resource_generator(
            self.n, self.num_resources, seed=self.seed
        )
        self.resource_amounts = create_resource_quantities(self.resource_ids, self.resource_lookup)

    def _initialize_agents(self):
        for agent in self.agents:
            # if no starting position was specified
            if not agent.x and not agent.y:
                agent.x = np.random.randint(self.n - 1)
                agent.y = np.random.randint(self.n - 1)
            self.agent_locations[agent.x][agent.y] = agent.id

    def create_map(self, obstacles):
        self._initialize_resources()
        if obstacles:
            self.add_obstacles()

        self._initialize_agents()

    def add_obstacles(self):
        # add a river
        pass

    def process_agent_actions(self, agents, actions):
        self.agents = agents
        for idx, agent in enumerate(agents):
            action_type = agent.get_action_type(actions[idx])
            if action_type == "move":
                self.move_agent(agent, actions[idx])
            elif action_type == "gather":
                self.gather_resources(agent)
            agent.add_inventory(agent.inventory)

    def move_agent(self, agent, action):
        agent.handle_action(action)
        self.agent_locations[agent.last_x, agent.last_y] = 0
        self.agent_locations[agent.x, agent.y] = 1

    def gather_resources(self, agent, gather_rate=10):
        if self.resource_ids[agent.x][agent.y] != 0:
            on_resource = self.resource_lookup[self.resource_ids[agent.x][agent.y]]
            print(f"agent standing on resource {on_resource.name} !!!: ",
                  self.resource_amounts[agent.x, agent.y])
            current_amount = self.resource_amounts[agent.x][agent.y]

            # if there is no more resource left, declare square empty
            if current_amount == 0:
                self.resource_ids[agent.x, agent.y] = 0

            gather_amount = int(min(10, current_amount))
            self.resource_amounts[agent.x][agent.y] -= gather_amount
            if on_resource.name in agent.inventory.keys():
                agent.inventory[on_resource.name] += gather_amount
            else:
                agent.inventory[on_resource.name] = gather_amount


if __name__ == '__main__':
    M = Map(200)
