from src.env.default_environments import SimpleEnvironment
from src.agents.simple.GatheringAgent import GatheringAgent
import time

if __name__ == '__main__':
    steps = 1000

    # set the environment with a default environment
    # steps is given for debug purposes for now - will change in the future
    Env = SimpleEnvironment()
    Env.max_timesteps = steps

    action_space = Env.action_space
    state_space = Env.state_space

    # using four GatheringAgents in the environment
    agents = [GatheringAgent() for _ in range(4)]

    # provide the environment with the agents
    Env.set_agents(agents)

    for episode in range(5):
        state, info = Env.reset()

        for i in range(steps):
            # environment is extremely fast - so use sleep for eval
            time.sleep(0.25)

            actions = [agent.select_action(state) for agent in agents]
            state, rewards, done = Env.step(actions)

            if True in done:
                break

        print(episode, Env.cumulative_rewards)