from gym_novel_gridworlds2.object import Object


class ScrapeTree(Object):
    def acted_upon(self, action_name, agent):
        if action_name == "scrape":
            if "plank" in agent.inventory:
                agent.inventory["plank"] += 1
            else:
                agent.inventory["plank"] = 1

    def placement_reqs(self, map_state, loc):
        return True