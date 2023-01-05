from gym_novel_gridworlds2.contrib.polycraft.objects.plastic_chest import PlasticChest

class BreakableChest(PlasticChest):
    def __init__(self, type="plastic_chest", loc=(0, 0), state="block", inventory=None, **kwargs):
        inventory = {"stick": 2, "block_of_diamond": 2, "block_of_titanium": 2, "rubber": 1, "tree_tap": 1}
        super().__init__(type, loc, state, inventory, **kwargs)

    def acted_upon(self, action_name, agent):
        if action_name == "break" or action_name == "collect":
            for item in self.inventory:
                if item in agent.inventory:
                    agent.inventory[item] += self.inventory[item]
                else:
                    agent.inventory[item] = self.inventory[item]
                self.inventory[item] = 0
