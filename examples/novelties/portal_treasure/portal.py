from gym_novel_gridworlds2.contrib.polycraft.objects import PolycraftObject
import pygame, os

# src: https://www.pngmart.com/image/34097
PORTAL_IMG = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "portal.png")
)
PORTAL_IMG = pygame.transform.scale(PORTAL_IMG, (20, 20))

class Portal(PolycraftObject):
    useable = True
    breakable = False

    def acted_upon(self, action_name, agent):
        if action_name == "use":
            if "treasure" in agent.inventory and agent.inventory["treasure"] > 0:
                agent.inventory["treasure"] -= 1
                agent.inventory.update({
                    "oak_log": agent.inventory.get("oak_log", 0) + 9
                })
    
    def get_img(self):
        return PORTAL_IMG
