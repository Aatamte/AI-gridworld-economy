from src.env.GridWorld import Map
from src.agents.BaseAgent import BaseAgent
from src.env.map_objects.Resources import default_resources

if __name__ == "__main__":
    agent = BaseAgent()
    x_size = 10
    y_size = 5
    map = Map(
        x_size=x_size,
        y_size=y_size,
        agents=[agent],
        resource_parameters=default_resources()
    )


    def test_x_dims():
        assert 10 == map.agent_locations.shape[0] == \
            map.resource_ids.shape[0] == map.resource_amounts.shape[0]

    def test_y_dims():
        assert 5 == map.agent_locations.shape[1] == \
            map.resource_ids.shape[1] == map.resource_amounts.shape[1]
