# Notes:
# Economy contains markets, the central bank,

class Economy:
    def __init__(
            self,

            goods_markets: list = None,
            services_markets: list = None,
            steps_per_year: int = 5
    ):
        self.steps_per_year = steps_per_year

        self.goods = goods_markets
        self.services = services_markets

    def process_agent_actions(self, actions):

        pass

