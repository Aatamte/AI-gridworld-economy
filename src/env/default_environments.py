from src.env.BaseEnvironment import BaseEnvironment


class SimpleEnvironment(BaseEnvironment):
    def __init__(self, **kwargs):
        super().__init__(
            size=(10, 10),
            **kwargs
        )


class Smith1962Environment(BaseEnvironment):
    def __init__(self):
        super().__init__(
            size=(100, 100),
            verbose=1,
            use_react=False,
            use_mongodb=False
        )


