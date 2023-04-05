import time
from src.env.GridWorldEconomy import GridWorldEconomy
from src.agents.HumanAgent import HumanAgent

if __name__ == '__main__':
    timesteps = 1000
    agent1 = HumanAgent()
    agent2 = HumanAgent()
    n = 50
    agents = [
        agent1,
        agent2
    ]

    Env = GridWorldEconomy(
        agents=agents,
        n=n
    )

    Env.reset()

    for i in range(timesteps):
        actions = []
        for agent in agents:
            actions.append(agent.random_action())
            agent.add_inventory(agent.inventory)
        time.sleep(2)
        Env.step(actions)