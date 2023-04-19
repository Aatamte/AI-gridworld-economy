from src.env.default_environments import SimpleEnvironment
from src.agents.simple.GatheringAgent import GatheringAgent
from src.agents.BaseAgent import ActionSpace
import time

if __name__ == '__main__':
    steps = 1000

    Env = SimpleEnvironment()

    # using four GatheringAgents in the environment
    my_agent = GatheringAgent()

    my_agent.action_space.add_buying_actions(
        "wood",
        50,
        1
    )

    print(my_agent.action_space_size)

    agents = [GatheringAgent() for _ in range(3)]
    agents.append(my_agent)

    # set the environment with a default environment
    # steps is given for debug purposes for now - will change in the future
    Env.set_agents(agents)

    for episode in range(5):
        state, info = Env.reset()

        for i in range(steps):
            # environment is extremely fast - so use sleep for eval
            time.sleep(0.05)

            actions = [agent.select_action(state) for agent in agents]
            state, rewards, done = Env.step(actions)

            if True in done:
                break

        print(episode, Env.cumulative_rewards)

    Env.close()