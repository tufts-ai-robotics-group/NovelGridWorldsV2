import gym

#modified version of code taken from:
#https://github.com/koulanurag/ma-gym/blob/master/ma_gym/envs/utils/action_space.py

class MultiAgentActionSpace(list):
    def __init__(self, agents_action_space):
        for x in agents_action_space:
            assert isinstance(x, gym.spaces.space.Space)

        super(MultiAgentActionSpace, self).__init__(agents_action_space)
        self._agents_action_space = agents_action_space

    def addActionSpace(self, agent_action_space):
        """adds another action space to the list"""
        assert isinstance(agent_action_space, gym.spaces.space.Space)
        self._agents_action_space.append(agent_action_space)

    def getActionAt(self, index):
        return self._agents_action_space[index].sample()

    def removeActionSpace(self, index):
        self._agents_action_space.pop(index)

    def sample(self):
        """ samples action for each agent from uniform distribution"""
        return [agent_action_space.sample() for agent_action_space in self._agents_action_space]