import numpy as np
from collections import deque
from dataclasses import dataclass
from src.env.Resources import default_resources


@dataclass
class Order:
    order_type: str
    order_market: str
    price: int
    quantity: int
    order_id: int = None


class ResourceMarketplace:
    def __init__(
            self,
            name
    ):
        self.name = name
        self.buy_orders = []
        self.sell_orders = []

    def get_quotes(self, order_type):
        if order_type == "buy":
            print(self.buy_orders)
        else:
            print(self.sell_orders)

    def execute_transaction(self):
        pass

    def insert_buy_order(self, order: Order):
        pass

    def insert_sell_order(self, order: Order):
        pass

    def insert_order(self, order: Order):
        print("got order")
        if order.order_type == "buy":
            self.buy_orders.append(order)
        else:
            self.sell_orders.append(order)

    def __repr__(self):
        return f"""
===============================================
market: {self.name}
buy orders: {self.buy_orders}
sell orders: {self.sell_orders}
===============================================
        """


class Marketplace:
    def __init__(
            self,
            resources: dict = None,
            markets = None
    ):
        self.default_resources = default_resources()
        self.markets = markets

        self.order_counter = 0

        if self.markets is None:
            self.markets = {}
            for market_name in self.default_resources.keys():
                self.markets[market_name] = ResourceMarketplace(
                    name=market_name
                )

    def send_order(self, order):
        order.order_id = self.order_counter
        print("send order")
        market = self.markets[order.order_market]
        market.insert_order(order)
        self.order_counter += 1

    def get_quotes(self, market_id):
        pass

    def create_ResourceMarket(self, name):
        self.markets[name] = ResourceMarketplace(
            name
        )

    def __repr__(self):
        return "".join([market.__repr__() for market in self.markets.values()])



if __name__ == '__main__':
    mplace = Marketplace()
