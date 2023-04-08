import time
from src.env.GridWorldEconomy import GridWorldEconomy
from src.agents.simple.RandomAgent import RandomAgent
from src.agents.simple.GatheringAgent import GatheringAgent
from src.agents.simple.HumanAgent import HumanAgent

if __name__ == '__main__':
    timesteps = 10000
    gridworld_size = (50, 50)

    Env = GridWorldEconomy(
        gridworld_size=gridworld_size
    )

    action_space = Env.action_space

    random_agents = [RandomAgent() for i in range(4)]
    test_agent = GatheringAgent()
    human = HumanAgent()
    agents = [test_agent, *random_agents]

    Env.set_agents(agents)

    prev_reward = 0

    for episode in range(5):
        state, info = Env.reset()

        for i in range(timesteps):
            actions = []
            for agent in random_agents:
                actions.append(agent.select_action(state))

            a = test_agent.select_action(state, prev_reward)

            state, rewards, dones = Env.step(
                [a, *actions]
            )
            prev_reward = rewards[0]
            print(rewards)

            #time.sleep(0.1)