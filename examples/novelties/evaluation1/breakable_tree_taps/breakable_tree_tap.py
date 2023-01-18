from gym_novel_gridworlds2.contrib.polycraft.objects.tree_tap import TreeTap
import pygame, os

IMG = pygame.image.load(
    os.path.join(os.path.dirname(__file__), "hopper.png")
)
IMG = pygame.transform.scale(IMG, (20, 20))


class BreakableTreeTap(TreeTap):
    def acted_upon(self, action_name, agent):
        # when the tree tap is broken, it will drop a rubber.
        # can't collect from it anymore.
        if action_name == "break":
            self.state = "floating"
            agent.add_to_inventory("rubber", 1)

    def get_img(self):
        return IMG
