import os
import random
import time

import numpy as np
from src.env.Visualizer import GridWorldVisualizer
from src.env.Map import Map
from src.env.Resources import Resource, default_resources
from src.env.Marketplace import Marketplace, Order
import logging
from src.agents.BaseAgent import BaseAgent

import threading
from src.react_visualization.backend.server import GridWorldReactServer
from matplotlib.colors import cnames

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
            gridworld_size: int = 100,
            use_react=True,
            verbose = 0,
            seed = None
    ):
        if not isinstance(agents, list):
            raise TypeError(
                "Please pass a list of BaseAgents. If only one agent, pass a list of length one"
            )
        # grid world size
        self.gridworld_size = gridworld_size
        self.n_agents = len(agents)
        self.agents = agents
        self._initialize_agents()
        self.use_react = use_react
        self.verbose = verbose
        self.seed = seed

        if self.seed:
            np.random.seed(self.seed)

        self.map = None
        self.current_timestep = None
        self.episode = 0

        self.resource_parameters = default_resources()
        self.marketplace = Marketplace()
        self.server = GridWorldReactServer()
        self.server.run()

    def _initialize_agents(self):
        names = {}
        used_colors = set()
        hex_colors = set(cnames.values())

        id = 0
        for idx, agent in enumerate(self.agents):
            agent.id = id
            agent.bounds = self.gridworld_size - 1
            if agent.color == None:
                agent.color = random.choice(list(hex_colors - used_colors))
                used_colors.add(agent.color)
            elif agent.color[0] != "#":
                try:
                    convert_to_hex_color = cnames[agent.color]
                    agent.color = convert_to_hex_color
                    used_colors.add(convert_to_hex_color)
                except:
                    agent.color = random.choice(list(hex_colors - used_colors))
                    used_colors.add(agent.color)

            # set agent name or
            # change agent name if more than one agent with the same name
            if agent.name not in names.keys():
                names[agent.name] = 0
            else:
                names[agent.name] += 1
                agent.name = agent.name + "_" + str(names[agent.name])

    def reset(self):
        self.current_timestep = 0
        self.episode += 1

        # reset each agent
        for agent in self.agents:
            agent.reset()

        # reset and initialize map configuration
        del self.map
        self.map = Map(self.gridworld_size, self.agents, self.resource_parameters, seed = self.seed)

        agent_locs = [agent.get_position() for agent in self.agents]
        hex_codes = {self.resource_parameters[r].id + 1: self.resource_parameters[r].color for r in self.resource_parameters}
        hex_codes[0] = "#8A9A5B"

        agent_names = {i: agent.name for i, agent in enumerate(self.agents)}

        self.server.send(
            {
                "agent_names": agent_names,
                "gridworld_color_lookup": hex_codes,
                "gridworld_y": self.gridworld_size,
                "gridworld_x": self.gridworld_size,
                "gridworld": self.map.resource_ids.tolist(),
                "agent_locations": agent_locs
            }
        )
        time.sleep(1)

        return self.get_state(), {}

    def calculate_rewards(self):
        agent_rewards = []
        for agent in self.agents:
            if len(agent.totals) > 2:
                agent_rewards.append(
                    agent.totals[self.current_timestep] - agent.totals[self.current_timestep - 1]
                )
            else:
                agent_rewards.append(0)
        return agent_rewards

    def get_state(self):
        return np.concatenate([self.map.resource_amounts.flatten().reshape(1, -1), self.map.agent_locations.flatten().reshape((1, -1))]).flatten().reshape(1, -1)

    def step(self, actions):
        self.map.process_agent_actions(self.agents, actions)

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

        if self.use_react:
            self.render_step()

        self.current_timestep += 1
        return self.get_state(), self.calculate_rewards(), [False for i in self.agents]

    def render_step(self):
        agent_locs = [agent.get_position() for agent in self.agents]

        agent_totals = []
        for i in range(self.current_timestep):
            agent_totals_dict = {}
            for agent in self.agents:
                agent_totals_dict[agent.name] = agent.totals[i]
            agent_totals.append(agent_totals_dict)

        self.server.send(
            {
                "agent_totals": agent_totals,
                "gridworld": self.map.resource_ids.tolist(),
                "agent_locations": agent_locs,
                "agent_data": [agent.inventory_history for agent in self.agents]
            }
        )


