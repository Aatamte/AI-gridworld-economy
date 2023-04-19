from dataclasses import dataclass
import numpy as np
from src.agents.BaseAgent import BaseAgent


@dataclass
class Order:
    price: int
    quantity: int
    agent: BaseAgent
    id: int = None
    entrystep: int = None
    open: bool = False


class OrderBook:
    """
    OrderBook is a class that allows agents to trade with each other
    """
    def __init__(self, product_name):
        self.product_name = product_name
        self.sell_orders = []
        self.buy_orders = []
        self.highest_bid_price = 0
        self.lowest_offer_price = np.Inf
        self.highest_bid_order: Order = None
        self.lowest_offer_order: Order = None
        self.order_count = 0
        self.order_logs = []

    def _can_order_be_executed(self, order: Order, is_buy_order: bool) -> bool:
        # for buy orders
        if is_buy_order:
            if len(self.sell_orders) == 0:
                return False
            else:
                if order.price >= self.lowest_offer_price:
                    self.execute(order, self.lowest_offer_order)
                    return True
        else:
            if len(self.buy_orders) == 0:
                return False
            else:
                if order.price <= self.highest_bid_price:
                    self.execute(order, self.highest_bid_order)
                    return True

    def is_order_legitimate(self, order: Order, is_buy_order: bool):
        print(order.agent.inventory)
        if is_buy_order:
            # agent does not have the capital to complete the order
            if order.agent.capital < order.price:
                return False
            else:
                return True
        else:
            # agent is trying to sell more than what they have
            if abs(order.quantity) > order.agent.inventory[self.product_name]:
                return False
            else:
                return True

    def add(self, order: Order):
        # check if agent has enough capital/product to make the order
        is_buy_order = True if order.quantity > 0 else False
        order_is_legitimate = self.is_order_legitimate(order, is_buy_order)

        if order_is_legitimate:
            order.id = self.order_count
            self.order_count += 1
            # if order can be executed immediately, do it
            order_was_executed = self._can_order_be_executed(order, is_buy_order)

            print(order_was_executed)

            if not order_was_executed:
                if is_buy_order:
                    self.buy_orders.append((order.id, order.price, order))
                    self.buy_orders = sorted(self.buy_orders, key=lambda x: x[1])
                    self.highest_bid_order = self.buy_orders[0][2]
                    self.highest_bid_price = self.highest_bid_order.price
                else:
                    self.sell_orders.append((order.id, order.price, order))
                    self.sell_orders = sorted(self.sell_orders, key=lambda x: x[1], reverse=True)
                    self.lowest_offer_order = self.sell_orders[0][2]
                    self.lowest_offer_price = self.lowest_offer_order.price

        print(self.buy_orders)
        print(self.sell_orders)

    def cancel(self, id):
        pass

    def execute(self, incoming_order: Order, book_order: Order):
        transaction_price = book_order.price

        if abs(incoming_order.quantity) <= abs(book_order.quantity):
            # complete order can be fulfilled
            transaction_quantity = abs(incoming_order.quantity)
        else:
            # a partial order can be fulfilled
            transaction_quantity = abs(incoming_order.quantity) - abs(book_order.quantity)
            residual_order = incoming_order
            residual_order.quantity -= transaction_quantity
            self.add(residual_order)

        print(transaction_price, transaction_quantity)
        # always execute on the book order price
        if incoming_order.quantity <= book_order.quantity:
            if book_order.quantity > 0:
                self.buy_orders.remove((book_order.id, book_order.price, book_order))
                # capital transaction
                incoming_order.agent.capital += transaction_price
                book_order.agent.capital -= transaction_price

                # inventory transaction
                incoming_order.agent.inventory[self.product_name] -= transaction_quantity
                book_order.agent.inventory[self.product_name] += transaction_quantity
            else:
                self.sell_orders.remove((book_order.id, book_order.price, book_order))
                #
                incoming_order.agent.capital -= transaction_price
                book_order.agent.capital += transaction_price

                incoming_order.agent.inventory[self.product_name] += transaction_quantity
                book_order.agent.inventory[self.product_name] -= transaction_quantity

        else:
            pass
        print(f"incoming order {incoming_order}")
        print(f"book order: {book_order}")
        print("transacting")
        transaction_str = f"agent '{incoming_order.agent.name}' transacted"

        print(transaction_str)
        self.order_logs.append(
            transaction_str
        )


if __name__ == '__main__':
    buy_agent = BaseAgent()
    sell_agent = BaseAgent()

    buy_agent.capital = 1000
    sell_agent.capital = 1000
    buy_agent.inventory["socks"] = 10
    sell_agent.inventory["socks"] = 10

    OB = OrderBook("socks")
    order_one = Order(price=90, quantity=1, agent=buy_agent)
    order_two = Order(price=80, quantity=-2, agent=sell_agent)
    #order_three = Order(price=)

    OB.add(order_one)
    OB.add(order_two)

    print(
        buy_agent.capital,
        buy_agent.inventory,
        sell_agent.capital,
        sell_agent.inventory
    )
