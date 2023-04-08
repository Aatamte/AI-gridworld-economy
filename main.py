import time
from src.env.GridWorldEconomy import GridWorldEconomy
from src.agents.simple.RandomAgent import RandomAgent
from src.agents.simple.GatheringAgent import GatheringAgent

if __name__ == '__main__':
    timesteps = 50
    gridworld_size = 100
    random_agents = [RandomAgent() for i in range(4)]
    test_agent = GatheringAgent()

    Env = GridWorldEconomy(
        gridworld_size=gridworld_size,
        agents=[test_agent, *random_agents]
    )

    prev_reward = 0

    for episode in range(20):
        state, info = Env.reset()

        for i in range(timesteps):
            actions = []
            for agent in random_agents:
                actions.append(agent.select_action(state))

            a = test_agent.select_action(state, prev_reward)

            print(a)
            time.sleep(0.5)
            state, rewards, dones = Env.step(
                [a, *actions]
            )
            prev_reward = rewards[0]
            print(rewards)

