import os
import time

import numpy as np
from src.env.Visualizer import GridWorldVisualizer
from src.env.Map import Map
from src.env.Resources import Resource, default_resources
import logging
import sys
from flask import Flask
import contextlib
with contextlib.redirect_stdout(None):
    import pygame

import threading
from src.Visualization.backend.server import GridWorldReactServer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)


class GridWorldEconomy:
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
        self.current_timestep = None
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

        self.server = GridWorldReactServer()
        self.server.run()

    def reset(self):
        self.current_timestep = 0
        self.map = Map(
            self.n,
            self.agents,
            self.resource_parameters
        )
        print(self.resource_parameters)
        agent_locs = [[agent.x, agent.y] for agent in self.agents]
        hex_codes = {self.resource_parameters[r].id + 1: self.resource_parameters[r].color for r in self.resource_parameters}
        hex_codes[0] = "#8A9A5B"
        print(hex_codes)
        self.server.update(
            {
                "gridworld_color_lookup": hex_codes,
                "gridworld_y": self.n,
                "gridworld_x": self.n,
                "gridworld": self.map.resource_ids.tolist(),
                "agent_locations": agent_locs
            }
        )
        time.sleep(1)

    def step(self, actions):
        self.map.exec_agent_actions(self.agents, actions)
        for agent in self.agents:
            logger.info(f"timestep: {self.current_timestep}  {agent.name} {agent.inventory}")
        if self.render:
            agent_locs = [[agent.x, agent.y] for agent in self.agents]

            server_data = {
                "gridworld": self.map.resource_ids.tolist(),
                "agent_locations": agent_locs,
                "agent_data": [agent.inventory_history for agent in self.agents]
            }
            self.server.update(server_data)
        self.current_timestep += 1

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
            agent.name = agent.name + "_" + str(names[agent.name])

    return agents
