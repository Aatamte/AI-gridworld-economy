from src.agents.BaseAgent import BaseAgent
from src.agents.complex.PPOAgent.PPO import DiscretePPO


class PPOAgent(BaseAgent):
    def __init__(self, use_pretrained: bool = False):
        super(PPOAgent, self).__init__()
        self.name = "PPO Agent"
        self.ppo_agent = None
        self.use_pretrained = use_pretrained

    def init_model(self):
        K_epochs = 100

        eps_clip = 0.2
        gamma = 0.99

        lr_actor = 0.001
        lr_critic = 0.005

        if self.use_pretrained:
            self.ppo_agent = DiscretePPO(
                self.state_space,
                self.n_actions,
                lr_actor,
                lr_critic,
                gamma,
                K_epochs,
                eps_clip
            )
            self.ppo_agent.load("C:\\Users\\aaron\\PycharmProjects\\gridworld-economy\\src\\agents\complex\\PPOAgent\\GatheringPPO_final.pth")
        else:
            self.ppo_agent = self.ppo_agent = DiscretePPO(
                self.state_space,
                self.n_actions,
                lr_actor,
                lr_critic,
                gamma,
                K_epochs,
                eps_clip
            )

    def select_action(self, state):
        return self.ppo_agent.select_action(state.flatten())

