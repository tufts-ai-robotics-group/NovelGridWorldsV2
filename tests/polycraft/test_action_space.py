import unittest

from gym_novel_gridworlds2.actions.action import PreconditionNotMetError

from gym_novel_gridworlds2.state import State
from gym_novel_gridworlds2.contrib.polycraft.actions.move import Move
from gym_novel_gridworlds2.contrib.polycraft.actions.break_item import Break
from gym_novel_gridworlds2.object.entity import Entity
from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import PolycraftObject
from gym_novel_gridworlds2.utils.MultiAgentActionSpace import MultiAgentActionSpace
from gym import spaces

class ActionSpaceTests(unittest.TestCase):
	def testBasicActionSpace(self):
		self.n_agents = 2
		self.action_space = MultiAgentActionSpace([spaces.Discrete(4) for _ in range(self.n_agents)])
		res = self.action_space.sample()
		print(res)

		self.action_space.addActionSpace(spaces.Discrete(10))
		res = self.action_space.sample()
		print(res)

		print(self.action_space.getActionAt(2))
		print(self.action_space.getActionAt(1))

		self.action_space.removeActionSpace(0)
		res = self.action_space.sample()
		print(res)

		self.action_space.removeActionSpace(0)
		res = self.action_space.sample()
		print(res)
