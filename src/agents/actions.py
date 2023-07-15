default_action_space_config = {
    "moving": True,
    "gathering": True,
    "trading": False,
    "building": False
}


class ActionHandler:
    def __init__(self):
        self.gather_amount = 10

    def process_actions(self, agents, actions, gridworld):
        for idx, agent in enumerate(agents):
            action = agent.action_space.decode(actions[idx])
            if isinstance(action, int):
                if action in [
                        ACTIONS.MOVE_NORTH,
                        ACTIONS.MOVE_SOUTH,
                        ACTIONS.MOVE_EAST,
                        ACTIONS.MOVE_WEST
                ]:
                    self.is_move(agent, action, gridworld)
                elif action == ACTIONS.GATHER:
                    self.is_gather(agent, gridworld, self.gather_amount)

    @staticmethod
    def is_move(agent, action, gridworld):
        last_x = agent.x
        last_y = agent.y
        if action == ACTIONS.MOVE_NORTH:
            agent.y -= 1
        elif action == ACTIONS.MOVE_SOUTH:
            agent.y += 1
        elif action == ACTIONS.MOVE_WEST:
            agent.x -= 1
        elif action == ACTIONS.MOVE_EAST:
            agent.x += 1

        # handle agent moving out of bounds
        if agent.x > gridworld.x_size - 1:
            agent.x = gridworld.x_size - 1
        elif agent.x < 0:
            agent.x = 0
        if agent.y > gridworld.y_size - 1:
            agent.y = gridworld.y_size - 1
        elif agent.y < 0:
            agent.y = 0

        if gridworld.agent_locations[agent.x][agent.y] == 0:
            gridworld.agent_locations[last_x, last_y] = 0
            gridworld.agent_locations[agent.x, agent.y] = agent.id
        else:
            agent.x = last_x
            agent.y = last_y

    @staticmethod
    def is_gather(agent, gridworld, max_gather=10):
        resource = gridworld[agent.x, agent.y].contains
        if resource:
            # if there is no more resource left, declare square empty
            if resource.current_amount != 0:
                gather_amount = int(min(max_gather, resource.gather_amount))
                resource.current_amount -= gather_amount
                agent.inventory[resource.name] = gather_amount
            else:
                gridworld.grid.resource_key[agent.x, agent.y] = 0

    def is_trade(self):
        pass


class ACTIONS:
    NOTHING = -1
    MOVE_NORTH = 0
    MOVE_SOUTH = 1
    MOVE_WEST = 2
    MOVE_EAST = 3
    GATHER = 4
    BUILD = 76
    BUY_FIVE = 5
    BUY_TEN = 6
    SELL_FIVE = 7
    SELL_TEN = 8
