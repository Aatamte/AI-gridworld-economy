# GridworldEconomy

This project was started to fill a gap in reinforcement learning frameworks for AI/economics research, given the potential impact that RL algorithims could have on the economy. It follows a gymnasium-style environment with reset() and step() methods, supports multi-agent training, and includes a React rendering of the environment.


# Example

Code snippet of a GatheringAgent(random action if previous reward == 0, repeat action if previous reward != 0) on a 10x10 grid with one resource - Wood. 

```Python
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

    # provide the environment with the agents for rendering, random starting states, trading, etc
    Env.set_agents(agents)

    for episode in range(100000):
        state, info = Env.reset()

        for i in range(steps):
            # environment is fast - using sleep to slow it down
            time.sleep(0.25)

            actions = [agent.select_action(state) for agent in agents]
            state, rewards, done = Env.step(actions)

            if True in done:
                break

        print(episode, Env.cumulative_rewards)
```

# Rendering in React

Below is an GIF of GatheringAgents (note: this is a larger grid, with more resources than the SimpleEnvironment included in the code snippet above).

![ai-gridworld-economy_example](https://user-images.githubusercontent.com/35645363/230498856-0a683546-f11e-4412-997f-1eb73682c35d.gif)


# Roadmap (TODO)
Features (estimated percent completed):

BaseEnvironment
 - map generation (25%)
 - resources (40%)
 - 
