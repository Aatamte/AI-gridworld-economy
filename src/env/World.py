import numpy as np
import pygame
from src.env.Visualizer import GridWorldVisualizer
from src.env.Map import Map
from src.env.Resources import Resource, default_resources


class TraditionalEconomy:
    """"""
    def __init__(
            self,
            agents,
            n: int = 100,
            max_timesteps: int = 1_000_000,
            render=True,
    ):
        if not isinstance(agents, list):
            raise TypeError(
                "incorrect type for agents, please pass a list of agents instead. If only one agent, pass a list of length one"
            )
        # grid world size = n x n
        self.n = n
        self.agents = initialize_agent_names(agents)
        self.number_agents = len(agents)
        self.max_timesteps = max_timesteps
        self.render = render

        self.map = None
        self.grid = np.zeros((n, n))
        self.agent_locations = np.zeros((n, n))
        self.natural_materials = np.zeros((n, n))

        # initialize agents and assigns agent ids
        self.agents_map = {}
        id = 0
        for agent in self.agents:
            agent.bounds = self.n - 1
            if agent.name not in self.agents_map:
                self.agents_map[agent.name] = agent
                agent.id = id
            id += 1

        self.resource_parameters = default_resources()

    def reset(self):
        self.map = Map(
            self.n,
            self.agents,
            self.resource_parameters
        )

        if self.render:
            self.vis = GridWorldVisualizer(self.n, self.resource_parameters)
            self.vis.reset(self.map)

    def step(self, actions):
        self.map.exec_agent_actions(self.agents, actions)
        for agent in self.agents:
            print(agent.name, agent.inventory)
        if self.render:
            self.vis.step(self.map)

    def close(self):
        pygame.quit()


def initialize_agent_names(agents):
    names = {}
    clrs = ["blue", "red", "green", "purple"]

    for idx, agent in enumerate(agents):
        agent.color = clrs[idx]
        if agent.name not in names.keys():
            names[agent.name] = 0
        else:
            names[agent.name] += 1
            agent.name = agent.name + str(names[agent.name])

    return agents
