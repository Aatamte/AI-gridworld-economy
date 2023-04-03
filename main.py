from src.env.World import TraditionalEconomy
from src.agents.HumanAgent import HumanAgents

if __name__ == '__main__':
    timesteps = 1000
    agent1 = HumanAgents()
    agent2 = HumanAgents()
    n = 10
    agents = [
        agent1,
        agent2
    ]
    Env = TraditionalEconomy(
        agents=agents,
        n=n
    )
    Env.reset()

    for i in range(timesteps):
        actions = []
        for agent in agents:
            actions.append(agent.select_action())

        Env.step(actions)