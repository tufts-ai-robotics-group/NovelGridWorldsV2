from gym_novel_gridworlds2.contrib.polycraft.objects.tree_tap import TreeTap

class BreakableTreeTap(TreeTap):
    def acted_upon(self, action_name, agent):
        if action_name == "collect" or action_name == "break":
            if "rubber" in agent.inventory:
                agent.inventory["rubber"] += 1
            else:
                agent.inventory.update({"rubber": 1})

