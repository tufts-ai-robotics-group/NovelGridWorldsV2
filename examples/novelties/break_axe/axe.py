from gym_novel_gridworlds2.contrib.polycraft.objects.iron_pickaxe import IronPickaxe
import pygame, os

# src: https://minecraft.fandom.com/wiki/Axe
AXE_IMG = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "Iron_Axe.png")
)
AXE_IMG = pygame.transform.scale(AXE_IMG, (20, 20))


class Axe(IronPickaxe):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = "block"
    
    def acted_upon(self, action_name, agent):
        if action_name == "break":
            self.state = "floating"
        return super().acted_upon(action_name, agent)

    def get_img(self):
        return AXE_IMG
