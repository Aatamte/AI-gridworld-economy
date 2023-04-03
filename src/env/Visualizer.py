import pygame
import numpy as np
from pygame.color import Color


class Colors:
    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)
    BLUE = (0, 0, 255)
    GREEN = (0, 51, 0)
    GRAY = (100, 100, 100)
    DIRT = (155, 118, 83)
    WOOD = (133, 94, 66)
    ORE = (51, 0, 85)
    EMPTY = (243, 239, 224)
    METAL = (70, 71, 62)


class GridWorldVisualizer:
    def __init__(self,
            n: int,
            resource_parameters
    ):
        self.n = n
        self.resource_parameters = resource_parameters
        self.resource_lookup = {r.id + 1: r for r in resource_parameters.values()}
        self.blockSize = 30
        self.half_blockSize = self.blockSize / 2
        self.WINDOW_WIDTH = n * self.blockSize
        self.WINDOW_HEIGHT = n * self.blockSize
        self.running = False
        pygame.init()
        pygame.display.init()

    def draw_cell(self, x, y, id, amount):
        rect = pygame.Rect(x * self.blockSize, y * self.blockSize, self.blockSize, self.blockSize)
        if id == 0:
            pygame.draw.rect(self.screen, Colors.EMPTY, rect)
        else:
            c = list(self.resource_lookup[id].color)
            intensity = 1 - (amount / self.resource_lookup[id].a_max)

            for i in range(3):
                c[i] = c[i] + (Colors.EMPTY[i] - c[i]) * (0.25 * intensity)

            pygame.draw.rect(self.screen, tuple(c), rect)

    def render(self, state):
        self.screen.fill(Colors.GREEN)
        self.render_resources(state.resource_ids, state.resource_amounts)

        self.render_agents(state.agents)

    def render_agents(self, agents):
        for agent in agents:
            pygame.draw.circle(self.screen, agent.color,
                               (agent.x * self.blockSize + self.half_blockSize, agent.y * self.blockSize + self.half_blockSize),
                               self.half_blockSize)

    def render_resources(self, ids, amounts):
        for i in range(self.n):
            for j in range(self.n):
                self.draw_cell(i, j, ids[i, j], amounts[i, j])

    def reset(self, gamemap):
        self.screen = pygame.display.set_mode((self.WINDOW_HEIGHT, self.WINDOW_WIDTH))
        self.clock = pygame.time.Clock()
        self.screen.fill(Colors.BLACK)
        self.render_resources(gamemap.resource_ids, gamemap.resource_amounts)
        pygame.event.pump()
        self.step(gamemap)

    def step(self, grid):
        # poll for events
        self.render(grid)
        pygame.event.pump()
        # pygame.QUIT event means the user clicked X to close your window
        self.clock.tick()
        # flip() the display to put your work on screen
        pygame.display.flip()
        pygame.display.update()
        pygame.event.pump()
