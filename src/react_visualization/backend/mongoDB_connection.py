from pymongo import MongoClient
from src.env.GridWorld import GridWorld
from pymongoarrow.api import Schema, write
import numpy as np

client = MongoClient("mongodb://localhost:27017")

example_gridworld_database = {

}


class MongoDBClient:
    def __init__(self, clear: bool = True):
        self.port = 5000
        self.mydb = client["gridworld_economy_database"]

        self.db_names = [
            "gridworld_database",
            "agent_database"
        ]

        self.unique_agent_id = 0
        self.agent_db_schema = Schema(
            {
                '_id': int,
                'name': str,
                'location': int
            }
        )
        self.agent_db = self.mydb["agent_database"]

       # self.gridworld_db_schema = Schema(
        #    {
         #       'episode': int,
          #      'step': int,
           #     'gridworld': np.ndarray
           # }
        #)
        self.unique_gridworld_id = 0
        self.gridworld_db = self.mydb["gridworld_database"]

        if clear:
            self.agent_db.drop()
            self.gridworld_db.drop()

    def send_gridworld(self, gridworld: GridWorld):
        # insert into database
        self.gridworld_db.insert_one(
            {
                '_id': self.unique_gridworld_id,
                'gridworld': gridworld.grid.resource_key.tolist(),
                'episode': gridworld.episode,
                'step': gridworld.curr_step,
            })
        self.unique_gridworld_id += 1

    def send_agents(self, agents):
        agent_info = []
        for agent in agents:
            agent_info.append(
                {
                    '_id': self.unique_agent_id,
                    'name': agent.name,
                    'location': agent.x
                }
            )
            self.unique_agent_id += 1

        self.agent_db.insert_many(
            agent_info
        )

    def clear_all_databases(self):
        self.gridworld_db.delete_many({})
        self.agent_db.delete_many({})

        self.gridworld_db.drop()
        self.agent_db.drop()


if __name__ == '__main__':
    pass