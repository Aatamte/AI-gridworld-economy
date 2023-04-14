from src.env.BaseEnvironment import BaseEnvironment


class SimpleEnvironment(BaseEnvironment):
    def __init__(self):
        super().__init__(
            gridworld_size=(10, 10)
        )