from .agent import Agent

class KeyboardAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def policy(self, observation):
        print(f">>>>>>>>> keyboard agent: Agent {self.name} can do these actions:")
        action_names = self.action_set.get_action_names()
        print(">>>>>>>>>> ", ', '.join([f"{index}: {name}" for (index, name) in enumerate(action_names)]))
        action = input(">>>>>>>>>> Enter your action (in number): ")
        return int(action)


    def get_observation(self):
        return []
