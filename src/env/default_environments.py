from src.env.BaseEnvironment import BaseEnvironment


class SimpleEnvironment(BaseEnvironment):
    def __init__(self, **kwargs):
        super().__init__(
            size=(10, 10),
            **kwargs
        )