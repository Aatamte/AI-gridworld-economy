import os
import time

import numpy as np
from src.env.Visualizer import GridWorldVisualizer
from src.env.Map import Map
from src.env.Resources import Resource, default_resources
from src.env.Marketplace import Marketplace, Order
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
        self.marketplace = Marketplace()

        self.server = GridWorldReactServer()
        self.server.run()

    def reset(self):
        self.current_timestep = 0
        for agent in self.agents:
            agent.reset()

        del self.map
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
        agent_names = {i: agent.name for i, agent in enumerate(self.agents)}
        self.server.update(
            {
                "agent_names": agent_names,
                "gridworld_color_lookup": hex_codes,
                "gridworld_y": self.n,
                "gridworld_x": self.n,
                "gridworld": self.map.resource_ids.tolist(),
                "agent_locations": agent_locs
            }
        )
        time.sleep(1)
        state = np.concatenate([self.map.resource_amounts.flatten().reshape(1, -1), self.map.agent_locations.flatten().reshape((1, -1))]).flatten().reshape(1, -1)

        return state, {}

    def step(self, actions):
        self.map.exec_agent_actions(self.agents, actions)
        for agent in self.agents:
            agent.inventory["gold"] += 0
            if agent.inventory["gold"] >= 1000000:
                self.marketplace.send_order(Order(
                    order_type="buy",
                    order_market="wood",
                    price=10,
                    quantity=1
                ))
            logger.info(f"timestep: {self.current_timestep}  {agent.name} {agent.inventory}")
            #logger.info(f"marketplace: {self.marketplace}")
        if self.render:
            agent_locs = [[agent.x, agent.y] for agent in self.agents]

            agent_totals = []
            for i in range(self.current_timestep):
                agent_totals_dict = {}
                for agent in self.agents:
                    agent_totals_dict[agent.name] = agent.totals[i]["total"]
                agent_totals.append(agent_totals_dict)

            server_data = {
                "agent_totals": agent_totals,
                "gridworld": self.map.resource_ids.tolist(),
                "agent_locations": agent_locs,
                "agent_data": [agent.inventory_history for agent in self.agents]
            }
            self.server.update(server_data)

        agent_rewards = []
        for agent in self.agents:
            if len(agent.totals) > 2:
                agent_rewards.append(
                    agent.totals[self.current_timestep]["total"] - agent.totals[self.current_timestep - 1]["total"]
                )
            else:
                agent_rewards.append(0)

        self.current_timestep += 1
        state = np.concatenate([self.map.resource_amounts.flatten().reshape(1, -1), self.map.agent_locations.flatten().reshape((1, -1))]).flatten().reshape(1, -1)
        return state, agent_rewards, [False for i in self.agents]



def initialize_agent_names(agents):
    names = {}
    clrs = ["blue", "red", "green", "purple", "gray", "darkgreen", "black"]

    for idx, agent in enumerate(agents):
        agent.color = clrs[idx]
        if agent.name not in names.keys():
            names[agent.name] = 0
        else:
            names[agent.name] += 1
            agent.name = agent.name + "_" + str(names[agent.name])

    return agents
