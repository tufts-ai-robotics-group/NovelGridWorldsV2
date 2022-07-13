from .polycraft_obj import PolycraftObject
import numpy as np


class Tree(PolycraftObject):
    def __init__(self, typee, loc=(0, 0), state="block", **kwargs):
        self.type = typee
        self.loc = loc  # update such that we update the 3D arr and add the item to it
        self.state = state  # two states: block and floating

        # potentially need to create an array of dependent tree taps such that we can delete all of
        # the tree taps attached to this on breaking

    def placement_reqs(self, loc):
        return True

    def acted_upon(self, action_name, agent):
        if action_name == "break":
            self.state = "floating"
            # obj1 = self.state.get_objects_at(np.add(self.loc, (0, -1)))
            # if len(obj1[0]) == 1:
            #     if obj1[0][0].type == "tree_tap":
            #         print(obj1[0][0])
            #         obj1[0][0].state = "floating"
            # obj2 = self.state.get_objects_at(np.add(self.loc, (0, 1)))
            # if len(obj2[0]) == 1:
            #     if obj2[0][0].type == "tree_tap":
            #         print(obj2[0][0])
            #         obj2[0][0].state = "floating"
            # obj3 = self.state.get_objects_at(np.add(self.loc, (1, 0)))
            # if len(obj3[0]) == 1:
            #     if obj3[0][0].type == "tree_tap":
            #         print(obj3[0][0])
            #         obj3[0][0].state = "floating"
            # obj4 = self.state.get_objects_at(np.add(self.loc, (-1, 0)))
            # if len(obj4[0]) == 1:
            #     if obj4[0][0].type == "tree_tap":
            #         print(obj4[0][0])
            #         obj4[0][0].state = "floating"

            # need to find a way to access the state such that the tree tap can get broken
