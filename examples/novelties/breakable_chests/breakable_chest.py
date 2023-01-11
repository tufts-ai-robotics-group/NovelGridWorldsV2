from gym_novel_gridworlds2.contrib.polycraft.objects.plastic_chest import PlasticChest
import pygame, os

BREAKABLE_CHEST_IMG = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "breakable_chest.png")
)
BREAKABLE_CHEST_IMG = pygame.transform.scale(BREAKABLE_CHEST_IMG, (20, 20))

CHEST_IMG = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "chest.png")
)
CHEST_IMG = pygame.transform.scale(CHEST_IMG, (20, 20))

class BreakableChest(PlasticChest):
    def __init__(self, type="plastic_chest", loc=(0, 0), state="block", inventory=None, **kwargs):
        self.inventory = {"stick": 2, "block_of_diamond": 2, "block_of_titanium": 2, "rubber": 1, "tree_tap": 1}
        super().__init__(type, loc, state, inventory, **kwargs)

    def acted_upon(self, action_name, agent):
        if action_name == "break":
            for item in self.inventory:
                if item in agent.inventory:
                    agent.inventory[item] += self.inventory[item]
                else:
                    agent.inventory[item] = self.inventory[item]
                self.inventory[item] = 0
            self.state = "floating"

    def get_img(self):
        if self.state == "floating":
            return BREAKABLE_CHEST_IMG
        else:
            return CHEST_IMG
