from dataclasses import dataclass
import numpy as np


@dataclass
class Order:
    price: int
    quantity: int
    id: int = None
    entrystep: int = None
    completed: bool = False


class OrderBook:
    def __init__(self):
        self.book = {}
        self.highest_bid_price = 0
        self.lowest_offer_price = np.Inf
        self.highest_bid_order = None
        self.highest_bid_order = None
        self.order_count = 0
        self.history = []

    def add(self, order: Order):
        order.id = self.order_count
        self.order_count += 1
        buy = True if order.quantity > 0 else False

        if buy:
            if order.price > self.highest_bid_price:
                pass

        else:
            if order.price < self.lowest_offer_price:
                pass

    def cancel(self, id):
        pass

    def execute(self):
        pass


class GoodsMarket:
    def __init__(
            self,
            name
    ):
        self.name = name
        self.order_book = OrderBook()

    def process_order(self, order: Order):
        pass

    def get_buyer_quotes(self):
        pass

    def get_seller_quotes(self):
        pass

    def execute_transaction(self):
        pass

    def get_logs(self):
        pass

    def __repr__(self):
        return f"""
===============================================
market: {self.name}
buy orders: {self.buy_orders}
sell orders: {self.sell_orders}
===============================================
        """


if __name__ == '__main__':
    OB = OrderBook()
    order_one = Order(

    )


