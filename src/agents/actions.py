

default_action_space_config = {
    "moving": True,
    "gathering": True,
    "trading": False,
    "building": False
}


def get_action_space_from_config(action_space_config, num_resources):
    action_space = 0
    for key, value in action_space_config.items():
        if not value:
            continue
        else:
            if key == "moving":
                action_space += 4
            elif key == "gathering":
                action_space += 1
            elif key == "trading":
                action_space += 10 * num_resources
    return action_space


def get_action_space_lookup_from_config(action_space_config):
    """

    """
    action_lookup = {}
    idx = 0
    for key, value in action_space_config.items():
        if not value:
            continue
        else:
            if key == "moving":
                action_lookup[idx] = ACTIONS.MOVE_NORTH
                idx += 1
                action_lookup[idx] = ACTIONS.MOVE_SOUTH
                idx += 1
                action_lookup[idx] = ACTIONS.MOVE_WEST
                idx += 1
                action_lookup[idx] = ACTIONS.MOVE_EAST
                idx += 1
            elif key == "gathering":
                action_lookup[idx] = ACTIONS.GATHER
                idx += 1
            elif key == "trading":
                pass
    return action_lookup


class ActionHandler:
    def __init__(
            self,
            map_size,
            config: dict = None,
    ):
        self.map_size = map_size
        self.gather_amount = 10

        # use default config if none provided
        if config is None:
            self.config = default_action_space_config
        else:
            self.config = config

        self.action_lookup = get_action_space_lookup_from_config(self.config)

    def process_actions(self, agents, actions, gridworld):
        decoded_actions = [self.action_lookup[action] for action in actions]
        for idx, agent in enumerate(agents):
            action = decoded_actions[idx]
            if action in [
                    ACTIONS.MOVE_NORTH,
                    ACTIONS.MOVE_SOUTH,
                    ACTIONS.MOVE_EAST,
                    ACTIONS.MOVE_WEST
            ]:
                self.move_agent(agent, action, gridworld)
            elif action == ACTIONS.GATHER:
                pass
                self.gather_resources(agent, gridworld, self.gather_amount)
            agent.add_inventory(agent.inventory)

    def move_agent(self, agent, action, gridworld):
        agent.last_x = agent.x
        agent.last_y = agent.y
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
            gridworld.agent_locations[agent.last_x, agent.last_y] = 0
            gridworld.agent_locations[agent.x, agent.y] = agent.id
        else:
            agent.x = agent.last_x
            agent.y = agent.last_y

    def gather_resources(self, agent, gridworld, max_gather=10):
        resource = gridworld[agent.x, agent.y].contains
        if resource:
            # if there is no more resource left, declare square empty
            if resource.current_amount != 0:
                gather_amount = int(min(max_gather, resource.gather_amount))
                resource.current_amount -= gather_amount
                if resource.name in agent.inventory.keys():
                    agent.inventory[resource.name] += gather_amount
                else:
                    agent.inventory[resource.name] = gather_amount
            else:
                gridworld.grid.resource_key[agent.x, agent.y] = 0


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


class MOVINGACTIONS:
    MOVE_NORTH = 0
    MOVE_SOUTH = 1
    MOVE_WEST = 2
    MOVE_EAST = 3


example_config = {
    "move": ["North"]
}


class ActionSpace:
    def __init__(
            self,
            config
    ):
        self.config = config
        self.lookup = {}
        idx = 0
        for key, value in self.config.items():
            if not value:
                continue
            else:
                if key == "moving":
                    self.lookup[idx] = ACTIONS.MOVE_NORTH
                    idx += 1
                    self.lookup[idx] = ACTIONS.MOVE_SOUTH
                    idx += 1
                    self.lookup[idx] = ACTIONS.MOVE_WEST
                    idx += 1
                    self.lookup[idx] = ACTIONS.MOVE_EAST
                    idx += 1
                elif key == "gathering":
                    self.lookup[idx] = ACTIONS.GATHER
                    idx += 1
                elif key == "trading":
                    pass

    def add(self):
        pass