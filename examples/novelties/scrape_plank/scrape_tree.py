from gym_novel_gridworlds2.object import Object


class ScrapeTree(Object):
    def acted_upon(self, action_name, agent):
        if action_name == "scrape":
            print("HERE")
            if "planks" in agent.inventory:
                agent.inventory["planks"] += 1
            else:
                agent.inventory["planks"] = 1

    @staticmethod
    def placement_reqs(map_state, loc):
        return True