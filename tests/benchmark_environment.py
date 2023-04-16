from src.env.default_environments import BaseEnvironment
from src.agents.simple.RandomAgent import RandomAgent
import time
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from tqdm import tqdm

"""
calculates the time to run the BaseEnvironment with differing numbers of RandomAgents and
GridWorld sizes. outputs a matplotlib plot

main() will run a performance evaluation with varying step sizes, numbers of agents, and grid sizes
"""


def run_example(steps: int, num_episodes: int, num_agents: int, size: tuple = (10, 10)) \
        -> [np.ndarray, np.ndarray]:
    """
    full == True:
        records the time it takes for every episode and every step

    full == False:
        records the time it takes for every episode and automatically calculates the means for the steps
    """
    counter = time.perf_counter
    agents = [RandomAgent() for _ in range(num_agents)]
    env = BaseEnvironment(size=size, use_react=False)
    env.set_agents(agents)
    env.max_timesteps = steps
    episode_performance = np.zeros((num_episodes,))
    steps_performance = np.zeros((num_episodes, steps))
    for episode in range(num_episodes):
        episode_tic = counter()
        state, info = env.reset()
        for i in range(steps):
            step_tic = counter()
            state, rewards, done = env.step([agent.select_action(state) for agent in agents])
            step_toc = counter()
            steps_performance[episode][i] = step_toc - step_tic
            if True in done:
                break
        episode_toc = counter()
        episode_performance[episode] = (episode_toc - episode_tic)
    return episode_performance, steps_performance


def main():
    # constants that are not tested but could be manually
    static_num_episodes = 10

    # constants to test impact of other variables
    static_step_size = 500
    static_grid_size = (25, 25)
    static_num_agents = 2

    # testing parameters for each possible test

    step_size_skip = 2
    starting_step_size = 100
    ending_step_size = 200

    num_agents_skip = 3
    starting_num_agents = 1
    ending_num_agents = 50

    grid_size_skip = (10, 10)
    starting_grid_size = (5, 5)
    ending_grid_size = (200, 200)

    # set to false if you dont want to test
    vary_step_size = True
    vary_num_agents = True
    vary_grid_sizes = True

    subplot_titles = []

    if vary_step_size:
        subplot_titles.append(
            "step size vs time"
        )
    if vary_num_agents:
        subplot_titles.append(
            "number of agents vs time"
        )
    if vary_grid_sizes:
        subplot_titles.append(
            "grid sizes vs time"
        )

    fig = make_subplots(
        rows=1,
        cols=sum([bool(x) for x in [vary_step_size, vary_num_agents, vary_grid_sizes]]),
        shared_yaxes=True,
        subplot_titles=tuple(subplot_titles),

    )
    col = 1
    """
    first evaluation is on step sizes
    """
    if vary_step_size:
        step_size_performance = []
        for _step_size in tqdm(range(starting_step_size, ending_step_size, step_size_skip)):
            step_size_performance.append(
                run_example(
                    _step_size,
                    static_num_episodes,
                    static_num_agents,
                    size=static_grid_size
                )[0].mean()
            )

        fig.add_trace(
            go.Scatter(
                x=np.arange(starting_step_size, ending_step_size, step_size_skip),
                y=step_size_performance
            ),
            row=1, col=col
        )
        col += 1

    if vary_num_agents:
        num_agents_performance = []
        for num_agents in tqdm(range(starting_num_agents, ending_num_agents, num_agents_skip)):
            num_agents_performance.append(
                run_example(
                    static_step_size,
                    static_num_episodes,
                    num_agents,
                    size=static_grid_size
                )[0].mean()
            )

        fig.add_trace(
            go.Scatter(
                x=np.arange(starting_num_agents, ending_num_agents, num_agents_skip),
                y=num_agents_performance
            ),
            row=1, col=col
        )
        col += 1

    if vary_grid_sizes:
        """
        NOTE: due to 2 dimensions in the size parameter of BaseEnvironment, 
        the performance evaluation of increasing grid sizes will be inclusive of possible 
        starting and ending sizes. For example:

        grid_size_skip = (1, 1)
        starting_grid_size = (1, 1)
        ending_grid_size = (2, 5)
        
        would test [(1, 1), (2, 2), (2, 3), (2, 4), (2, 5)]
        
        it does not stop once a single axis reaches the ending specification, and continues until
        both axis reaches the ending specification
        """
        grid_size_params = []
        tmp_size = list(starting_grid_size)
        end_condition_x = False
        end_condition_y = False
        while True:
            grid_size_params.append(tmp_size.copy())

            if tmp_size[0] + grid_size_skip[0] < ending_grid_size[0]:
                tmp_size[0] += grid_size_skip[0]
            else:
                end_condition_x = True

            if tmp_size[1] + grid_size_skip[1] < ending_grid_size[1]:
                tmp_size[1] += grid_size_skip[1]
            else:
                end_condition_y = True

            if end_condition_y and end_condition_x:
                break
        grid_size_performance = []
        for size_param in tqdm(grid_size_params):
            grid_size_performance.append(
                run_example(
                    static_step_size,
                    static_num_episodes,
                    static_num_agents,
                    size=tuple(size_param)
                )[0].mean()
            )

        fig.add_trace(
            go.Scatter(
                x=[str(x) for x in grid_size_params],
                y=grid_size_performance,
            ),
            row=1, col=col
        )
        col += 1

    fig.show()


if __name__ == '__main__':
    main()