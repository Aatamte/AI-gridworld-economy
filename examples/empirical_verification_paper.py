import random
from src.env.default_environments import Smith1962Environment
import numpy as np
import plotly.graph_objs as go
from src.env.environment_enhancements.Marketplace import Marketplace
from src.agents.llm_based.GPTAgent import SellerGPTAgent, BuyerGPTAgent
import time
import openai
from scipy.optimize import fsolve


def plot_supply_demand(demand_function, supply_function):
    go.Figure(
        data=[
            go.Scatter(
                y=demand_function,
                line={"shape": 'hv'}
            ),
            go.Scatter(
                y=supply_function,
                line={"shape": 'hv'}
            )
        ]
    ).show()


def create_agents(s_curve, d_curve, n_agents):
    all_agents = []
    n_repeats = 2
    for idx in range(n_agents):
        for repeats in range(n_repeats):
            print(f"setup: {idx}")
            time.sleep(1)
            try:
                buying_agent = BuyerGPTAgent(d_curve[idx])
                all_agents.append(buying_agent)
                selling_agent = SellerGPTAgent(s_curve[idx])
                all_agents.append(selling_agent)
            except:
                pass

    return all_agents


def main():
    API_key = "sk-__"
    openai.api_key = API_key
    env = Smith1962Environment()
    mark = Marketplace(["Banana"])
    env.add_enhancement(mark)

    n_agents = 10

    def demand_func(x):
        return 150 - (1 * x)

    def supply_func(x):
        return (1 * x) + 140

    demand_function = np.array([demand_func(x) for x in range(n_agents)], dtype=int)
    supply_function = np.array([supply_func(x) for x in range(n_agents)], dtype=int)
    plot_supply_demand(demand_function, supply_function)

    def func(x):
        return demand_func(x) - supply_func(x)

    equilibrium = supply_func(fsolve(func, np.arange(n_agents))[0])
    print(equilibrium)

    agents = create_agents(supply_function, demand_function, n_agents)
    env.set_agents(agents)
    state = env.reset()
    tot_iterations = 0
    max_rounds = 10
    convergence_list = []
    period_convergence_list = []
    best_bids = []
    best_asks = []
    for trading_period in range(1, max_rounds + 1):
        print(trading_period)
        trading_period_alpha = []
        random.shuffle(agents)
        for agent in agents:
            #if isinstance(agent, SellerGPTAgent) and agent.inventory["Banana"] == 0:
            #    print(agent.name, "Skipped")
            #    continue
            #if isinstance(agent, BuyerGPTAgent) and agent.inventory.capital < agent.inventory.starting_capital:
            #    print(agent.name, "Skipped")
            #    continue
            try:
                market = env.environment_enhancements["MarketPlace"].markets["Banana"]
                price_history = market.history["price"].values
                alpha = 0
                if len(price_history) != 0:
                    std_around_eq = abs(price_history - equilibrium) ** 2
                    std_around_eq = np.sqrt(np.mean(std_around_eq))
                    alpha = 100 * (std_around_eq / equilibrium)
                convergence_list.append(alpha)
                trading_period_alpha.append(alpha)
                asks_orderbook = market.get_sellers()
                bids_orderbook = market.get_buyers()
                if len(asks_orderbook) != 0:
                    best_asks.append(int(asks_orderbook[0]))
                else:
                    best_asks.append(0)

                if len(bids_orderbook) != 0:
                    best_bids.append(int(bids_orderbook[0]))
                else:
                    best_bids.append(0)

                state = {
                    "max_trading_periods": max_rounds,
                    "trading_period": trading_period,
                    "bids_orderbook": bids_orderbook,
                    "asks_orderbook": asks_orderbook,
                    "previous_transactions": price_history
                }
                print("=======================")
                print(alpha)
                print(trading_period, tot_iterations / (max_rounds * len(agents)))
                print(agent.name, ": ")
                action = agent.select_action(state)
                print(action)
                _ = env.step([action])
                tot_iterations += 1
            except:
                tot_iterations += 1
            print(best_bids, best_asks)
        period_convergence_list.append(trading_period_alpha)

        market = env.environment_enhancements["MarketPlace"].markets["Banana"]
        print(market)
        price_history = env.environment_enhancements["MarketPlace"].markets["Banana"].history
        print(price_history)
        print(price_history["price"].mean())
        sum_errors = sum([agent.errors_in_GPT for agent in agents])
        print(sum_errors)
        sum_errors = sum([agent.critical_errors_in_GPT for agent in agents])
        print(sum_errors)
        go.Figure(
            go.Scatter(
                y=price_history["price"]
            )
        ).show()

        go.Figure(
            go.Scatter(
                y=convergence_list
            )
        ).show()
        for el in period_convergence_list:
            print(np.mean(el))

        print(best_bids)
        print(best_asks)

        go.Figure(
            data=[
                go.Scatter(
                x=np.arange(len(best_asks)),
               y=best_asks
            ),
                go.Scatter(
                    x = np.arange(len(best_bids)),
                    y=best_bids
                )
            ]
        ).show()

        go.Figure(
            data=[
            go.Scatter(
               y=el
            ) for el in period_convergence_list]
        ).show()


if __name__ == '__main__':
    main()



