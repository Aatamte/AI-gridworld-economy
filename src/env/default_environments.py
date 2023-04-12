from src.env.GridWorldEconomy import GridWorldEconomy


class SimpleEnvironment(GridWorldEconomy):
    def __init__(self):
        super().__init__(
            gridworld_size=(10, 10)
        )