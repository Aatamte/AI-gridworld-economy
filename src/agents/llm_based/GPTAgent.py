from src.agents.BaseAgent import BaseAgent
import openai
import re
import numpy as np

BUYER_PROMPT = """
The following are instructions for participating in a simulation:
You are a buyer in a competitive market simulation. You will be given a card containing a number, known only to you, which represents the maximum price you are willing to pay for one unit of the fictitious commodity. You are entirely willing to pay just this price for the commodity rather than have your wants go unsatisfied. However, the difference between the number on your card and the actual contract price is considered a pure profit. You are aware that there are other buyers and sellers. At the beginning of each round, you will be given current market information including the orderbook, previous transactions, and the card with your price.
An example of the format of this information is provided below:

“””
ROUND: 1 of 3
PRICE ON YOUR CARD: $10
MARKET INFORMATION:
AVERAGE OF LAST 5 TRANSACTIONS: $10
AVERAGE OF ALL 50 TRANSACTIONS: $10
ORDERBOOK:
BEST BID: $10
BEST ASK: $10
“””
Remember, you cannot buy for a price greater than what is on your card. Additionally, the profit is calculated by (PRICE ON YOUR CARD - SALE PRICE). For example, if SALE PRICE is $100 and the PRICE ON YOUR CARD is $110, the calculation would be ($110 - $100) = $10.
Afterwards, you can choose two options: either (A) make an offer to buy a unit of the good for a particular price, or (B) skip your turn. You would rather have an order in the orderbook at an advantageous price than skip your turn.
If you choose option A, follow this format:
“””
ACTION: buy for $(price)
REASON: …
“””

If you choose option B, follow this format:
“””
ACTION: skip
REASON: …
“””

Are you ready? The simulation will begin when you say that you are ready to begin."""

SELLER_PROMPT = """
The following are instructions for participating in a simulation:
You are a seller in a competitive market simulation. You will be given a card containing a number, known only to you, which represents the minimum price you are willing to sell one unit of the fictitious commodity. You are entirely willing to sell one unit of the commodity at this price rather than fail to make a sale. However, the difference between the number on your card and the actual contract price is considered a pure profit. You are aware that there are other buyers and sellers. At the beginning of each round, you will be given current market information including the orderbook, previous transactions, and the card with your price.
An example of the format of this information is provided below:

“””
ROUND: 1 of 3
PRICE ON YOUR CARD: $10
MARKET INFORMATION:
AVERAGE OF LAST 5 TRANSACTIONS: $10
AVERAGE OF ALL 50 TRANSACTIONS: $10
ORDERBOOK:
BEST BID : $10
BEST ASK: $10
“””

Remember, you cannot sell for a price lower than what is on your card. Additionally, the profit is calculated by (SALE PRICE - PRICE ON YOUR CARD). For example, if you sold the good for $10, the calculation would be (10 - 9) = 1.
Afterwards, you can choose two options: either (A) make an offer to sell a unit of the good for a particular price, or (B) skip your turn. You would rather have an order in the orderbook at an advantageous price than skip your turn.
If you choose option A, follow this format:
“””
ACTION: sell for $(price)
REASON: …
“””

If you choose option B, follow this format:
“””
ACTION: skip
REASON: …
“””

Are you ready? The simulation will begin when you say that you are ready to begin."""

buyer_temp = 1
seller_temp = 1


def format_state_to_string(trading_period, max_trading_periods, bids_orderbook, asks_orderbook, price_threshold, previous_transactions):
    prev_transactions_string = "$" + ", $".join([str(val) for val in previous_transactions]) if len(previous_transactions) != 0 else "None"
    average_transaction_string = f"${np.round(np.mean(previous_transactions[-5:]), 2)}"if len(previous_transactions) != 0 else "None"
    bids_string = f"${', $'.join(bids_orderbook[:1])}" if len(bids_orderbook) != 0 else "None"
    asks_string = f"${', $'.join(asks_orderbook[:1])}" if len(asks_orderbook) != 0 else "None"
    state_string = f"""
ROUND: {trading_period} of {max_trading_periods}
PRICE ON YOUR CARD: ${price_threshold}
MARKET INFORMATION:
AVERAGE OF LAST 5 TRANSACTIONS: {average_transaction_string}
AVERAGE OF ALL {len(previous_transactions)} TRANSACTIONS: {f"${np.round(np.mean(previous_transactions), 2)}"if len(previous_transactions) != 0 else "None"}
ORDERBOOK:
BEST BID: {bids_string}
BEST ASK: {asks_string}"""
    print(state_string)
    return state_string


power = 20


class BuyerGPTAgent(BaseAgent):
    def __init__(self, price_threshold: int):
        super().__init__()
        self.buyer_temp = 1
        self.inventory.starting_capital = price_threshold * power
        self.name = "buying agent"
        self.inventory.starting_inventory = {"Banana": 0}
        self.price_threshold = price_threshold
        self.conversation = [{'role': 'system', 'content': BUYER_PROMPT}]
        self.model_id = "gpt-3.5-turbo-0613"
        response = openai.ChatCompletion.create(model=self.model_id, messages=self.conversation, temperature=buyer_temp)
        self.conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
        print(response["choices"][-1]["message"]["content"])
        self.errors_in_GPT = 0
        self.critical_errors_in_GPT = 0

    def select_action(self, state_dict):
        # ask agent for action
        self.conversation.append({'role': 'user', 'content': format_state_to_string(price_threshold=self.price_threshold, **state_dict)})
        response = openai.ChatCompletion.create(model=self.model_id, messages=self.conversation, temperature=buyer_temp)
        self.conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
        # parse response from gpt
        action = self.parse_response_and_get_action(response)
        print(self.name, self.price_threshold, action)
        if action is None:
            return action
        else:
            #check if action is valid or invalid
            is_valid = self.is_valid_action(action)
            if is_valid:
                return action
            else:
                #agent suggested an invalid action
                buying_price = action[3][1]
                self.conversation.append(
                    {'role': 'user', 'content': f"The price you suggested {buying_price} is greater than your budget of {self.price_threshold}. Please choose a valid action"})
                response = openai.ChatCompletion.create(model=self.model_id, messages=self.conversation,
                                                        temperature=buyer_temp)
                self.conversation.append(
                    {'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
                action = self.parse_response_and_get_action(response)
                print(self.name, self.price_threshold, action)
                if action is None:
                    return action
                else:
                    # check if action is valid or invalid
                    is_valid = self.is_valid_action(action)
                    if is_valid:
                        return action
                    else:
                        self.critical_errors_in_GPT += 1
                        return None

    def is_valid_action(self, action):
        buying_price = action[3][1]
        if buying_price > self.price_threshold:
            self.errors_in_GPT += 1
            return False
        else:
            return True

    def parse_response_and_get_action(self, response):
        gpt_response = response["choices"][-1]["message"]["content"].split("\n")
        action_str = ""
        for item in gpt_response:
            if item[:6] == "ACTION":
                action_str = item
        if action_str == "ACTION: skip":
            return None
        else:
            if action_str[:15] == "ACTION: buy for":
                # find number in string through re
                price = re.findall(r'\d+', action_str)[0]
                action = (self.name, 1, "MarketPlace", ["Banana", int(price), 1])
                return action
            else:
                self.errors_in_GPT += 1
                return None


class SellerGPTAgent(BaseAgent):
    def __init__(self, price_threshold: int):
        super().__init__()
        self.inventory.starting_capital = 0
        self.name = "selling agent"
        self.inventory.starting_inventory = {"Banana": power}
        self.price_threshold = price_threshold
        self.conversation = [{'role': 'system', 'content': SELLER_PROMPT}]
        self.model_id = "gpt-3.5-turbo-0613"
        response = openai.ChatCompletion.create(model=self.model_id, messages=self.conversation, temperature=seller_temp)
        self.conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
        print(response["choices"][-1]["message"]["content"])
        self.errors_in_GPT = 0
        self.critical_errors_in_GPT = 0

    def select_action(self, state_dict):
        self.conversation.append({'role': 'user', 'content': format_state_to_string(price_threshold=self.price_threshold, **state_dict)})
        response = openai.ChatCompletion.create(model=self.model_id, messages=self.conversation, temperature=seller_temp)
        self.conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
        action = self.parse_response_and_get_action(response)
        print(self.name, self.price_threshold, action)
        if action is None:
            return action
        else:
            #check if action is valid or invalid
            is_valid = self.is_valid_action(action)
            if is_valid:
                return action
            else:
                #agent suggested an invalid action
                selling_price = action[3][1]
                self.conversation.append(
                    {'role': 'user', 'content': f"The price you suggested {selling_price} is lower than your minimum selling price of {self.price_threshold}. Please choose a valid action"})
                response = openai.ChatCompletion.create(model=self.model_id, messages=self.conversation,
                                                        temperature=buyer_temp)
                self.conversation.append(
                    {'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
                action = self.parse_response_and_get_action(response)
                print(self.name, self.price_threshold, action)
                if action is None:
                    return action
                else:
                    # check if action is valid or invalid
                    is_valid = self.is_valid_action(action)
                    if is_valid:
                        return action
                    else:
                        self.critical_errors_in_GPT += 1
                        return None

    def is_valid_action(self, action):
        selling_price = action[3][1]
        if selling_price < self.price_threshold:
            self.errors_in_GPT += 1
            return False
        else:
            return True

    def parse_response_and_get_action(self, response):
        gpt_response = response["choices"][-1]["message"]["content"].split("\n")
        action_str = ""
        for item in gpt_response:
            if item[:6] == "ACTION":
                action_str = item
        if action_str == "ACTION: skip":
            return None
        else:
            if action_str[:16] == "ACTION: sell for":
                # find number in string through re
                price = re.findall(r'\d+', action_str)[0]
                action = (self.name, 1, "MarketPlace", ["Banana", int(price), -1])
                return action
            else:
                self.errors_in_GPT += 1
                return None