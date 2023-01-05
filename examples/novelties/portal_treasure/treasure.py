from gym_novel_gridworlds2.contrib.polycraft.objects import PolycraftObject
import pygame, os

# src: https://www.pngwing.com/en/free-png-zdolx
TREASURE_IMG = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "treasure.png")
)
TREASURE_IMG = pygame.transform.scale(TREASURE_IMG, (20, 20))


class Treasure(PolycraftObject):
    def get_img(self):
        return TREASURE_IMG
