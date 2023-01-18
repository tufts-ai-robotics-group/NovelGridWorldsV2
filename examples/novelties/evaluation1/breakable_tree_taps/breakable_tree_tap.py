from gym_novel_gridworlds2.contrib.polycraft.objects.tree_tap import TreeTap

class BreakableTreeTap(TreeTap):
    def acted_upon(self, action_name, agent):
        # when the tree tap is broken, it will drop a rubber.
        # can't collect from it anymore.
        if action_name == "break":
            self.state = "floating"
            agent.add_to_inventory("rubber", 1)
