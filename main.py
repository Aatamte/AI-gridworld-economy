import time
from src.env.GridWorldEconomy import GridWorldEconomy
from src.agents.simple.RandomAgent import RandomAgent
from src.agents.simple.GatheringAgent import GatheringAgent

if __name__ == '__main__':
    timesteps = 1000
    n = 50
    random_agents = [RandomAgent() for i in range(4)]
    test_agent = GatheringAgent()

    print([test_agent, *random_agents])
    Env = GridWorldEconomy(
        agents=[test_agent, *random_agents],
        n=n
    )

    prev_reward = 0

    for episode in range(10):
        state, info = Env.reset()

        for i in range(timesteps):
            actions = []
            for agent in random_agents:
                actions.append(agent.select_action(state))
                agent.add_inventory(agent.inventory)

            a = test_agent.select_action(state, prev_reward)
            test_agent.add_inventory(test_agent.inventory)

            print(a)
            time.sleep(0.05)
            state, rewards, dones = Env.step(
                [a, *actions]
            )
            prev_reward = rewards[0]
            print(rewards)

