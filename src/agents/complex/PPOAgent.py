from src.agents.BaseAgent import BaseAgent
import torch
import torch.nn as nn
from torch.distributions import MultivariateNormal
from torch.distributions import Categorical
import numpy as np
import random
from collections import namedtuple, deque

import torch
import torch.nn.functional as F
import torch.optim as optim


class PPOAgent(BaseAgent):
    def __init__(self, map_size):
        super(PPOAgent, self).__init__()
        self.name = "PPO Agent"


    def select_action(self, state):
        a = 0
        return a

    def update(self, s, a, r, s_, dw):
        pass

