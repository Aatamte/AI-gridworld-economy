

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


def get_action_space_value_settings_from_config(action_space_config):
    """

    """
    action_settings = {}
    idx = 0
    for key, value in action_space_config.items():
        if not value:
            continue
        else:
            if key == "moving":
                action_settings[idx] = ""
                pass
            elif key == "gathering":
                pass
            elif key == "trading":
                pass


class ACTIONS:
    MOVE_NORTH = 1
    MOVE_SOUTH = 2
    MOVE_WEST = 3
    MOVE_EAST = 4
    GATHER = 5