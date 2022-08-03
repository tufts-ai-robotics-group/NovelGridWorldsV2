import numpy as np
from .agent import Agent


class Pogoist(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.isMoving = False
        self.policy_step = 0
        self.rotate_step = 0
        self.starting_step_safe = 0
        self.doingSafeRoute = False

    def policy(self, observation):
        """
        Implements a basic pogoist algorithm as described below:
        """

        # find tree, teleport to said tree
        # break tree
        # move forward to get log
        # repeat last 3 steps 2 more times

        # teleport to crafting table
        # craft tree tap

        # teleport to tree
        # teleport 1 coord behind where it is
        # place tree tap
        # collect rubber

        # teleport to diamond ore
        # break it
        # move forward to get it
        # repeat last 3 steps again

        # teleport to platinum
        # break it
        # move forward to get it
        # repeat last 3 steps again

        # teleport to entity 103
        # trade platinum for titanium twice

        # teleport to crafting table
        # crafts pogostick

        # if self.isMoving:
        #     self.isMoving = False
        #     action_sets = self.action_set.get_action_names()
        #     to_do = self.get_action_space().sample()
        #     while to_do == action_sets.index("NOP"):
        #         to_do = self.get_action_space().sample()
        #     return to_do
        # else:  # skip every other turn
        #     self.isMoving = True
        #     action_sets = self.action_set.get_action_names()
        #     return action_sets.index("NOP")

        ent = self.state.get_entity_by_id(102)

        if self.isMoving:
            action_sets = self.action_set.get_action_names()
            if self.doingSafeRoute == False:
                if self.rotate_step == 4:
                    self.policy_step -= 1  # block obviously gone, must find new one
                    self.rotate_step = 0
                self.isMoving = False
                if (
                    self.policy_step == 0
                    or self.policy_step == 4
                    or self.policy_step == 8
                    or self.policy_step == 19
                ):
                    objs = self.state.get_objects_of_type("oak_log")
                    if len(objs) > 0:
                        self.policy_step += 1
                        return action_sets.index(
                            "TP_TO_"
                            + str(objs[0].loc[0])
                            + ",17,"
                            + str(objs[0].loc[1])
                        )
                    else:
                        self.policy_step += 1
                        return action_sets.index("NOP")

                elif (
                    self.policy_step == 1
                    or self.policy_step == 5
                    or self.policy_step == 9
                    or self.policy_step == 20
                ):
                    vec = (0, 0)
                    if ent.facing == "NORTH":
                        vec = (-1, 0)
                    elif ent.facing == "SOUTH":
                        vec = (1, 0)
                    elif ent.facing == "WEST":
                        vec = (0, -1)
                    else:
                        vec = (0, 1)

                    new_loc = np.add(vec, ent.loc)
                    objs = self.state.get_objects_at(tuple(new_loc))
                    if len(objs[0]) > 0:
                        if objs[0][0].type != "oak_log":
                            self.rotate_step += 1
                            return action_sets.index("rotate_right")
                            # need to rotate until we are facing the oak log
                        else:
                            self.policy_step += 1
                            self.rotate_step = 0
                            return action_sets.index("NOP")
                            # do nothing as already facing the log, move onto next part of policy
                    else:
                        self.rotate_step += 1
                        return action_sets.index("rotate_right")
                        # need to rotate until we are facing the oak log
                elif (
                    self.policy_step == 2
                    or self.policy_step == 6
                    or self.policy_step == 10
                    or self.policy_step == 28
                    or self.policy_step == 32
                    or self.policy_step == 36
                    or self.policy_step == 40
                ):
                    self.policy_step += 1
                    return action_sets.index("break")
                elif (
                    self.policy_step == 3
                    or self.policy_step == 7
                    or self.policy_step == 11
                    or self.policy_step == 29
                    or self.policy_step == 33
                    or self.policy_step == 37
                    or self.policy_step == 41
                ):
                    self.policy_step += 1
                    return action_sets.index("forward")
                elif self.policy_step == 12 or self.policy_step == 46:
                    objs = self.state.get_objects_of_type("crafting_table")
                    if len(objs) > 0:
                        self.policy_step += 1
                        return action_sets.index(
                            "TP_TO_"
                            + str(objs[0].loc[0])
                            + ",17,"
                            + str(objs[0].loc[1])
                        )
                    else:
                        # will have to wait until crafting table is available
                        return action_sets.index("NOP")
                elif self.policy_step == 13 or self.policy_step == 47:
                    vec = (0, 0)
                    if ent.facing == "NORTH":
                        vec = (-1, 0)
                    elif ent.facing == "SOUTH":
                        vec = (1, 0)
                    elif ent.facing == "WEST":
                        vec = (0, -1)
                    else:
                        vec = (0, 1)

                    new_loc = np.add(vec, ent.loc)
                    objs = self.state.get_objects_at(tuple(new_loc))
                    if len(objs[0]) > 0:
                        if objs[0][0].type != "crafting_table":
                            self.rotate_step += 1
                            return action_sets.index("rotate_right")
                            # need to rotate until we are facing the crafting table
                        else:
                            self.policy_step += 1
                            self.rotate_step = 0
                            return action_sets.index("NOP")
                            # do nothing as already facing the log, move onto next part of policy
                    else:
                        self.rotate_step += 1
                        return action_sets.index("rotate_right")
                        # need to rotate until we are facing the crafting table
                elif (
                    self.policy_step == 14
                    or self.policy_step == 15
                    or self.policy_step == 16
                ):
                    self.policy_step += 1
                    return action_sets.index("craft_plank")
                elif self.policy_step == 17:
                    self.policy_step += 1
                    return action_sets.index("craft_stick")
                elif self.policy_step == 18:
                    self.policy_step += 1
                    return action_sets.index("craft_tree_tap")
                elif self.policy_step == 21:
                    self.policy_step += 1
                    return action_sets.index(
                        "TP_TO_" + str(ent.loc[0]) + ",17," + str(ent.loc[1])
                    )
                elif self.policy_step == 22:
                    self.policy_step += 1
                    return action_sets.index("select_tree_tap")
                elif self.policy_step == 23:
                    self.policy_step += 1
                    return action_sets.index("place_item")
                elif self.policy_step == 24:
                    self.policy_step += 1
                    return action_sets.index("collect")
                elif self.policy_step == 25:
                    self.policy_step += 1
                    return action_sets.index("select_iron_pickaxe")
                elif self.policy_step == 26 or self.policy_step == 30:
                    objs = self.state.get_objects_of_type("diamond_ore")
                    if len(objs) > 0:
                        self.policy_step += 1
                        return action_sets.index(
                            "TP_TO_"
                            + str(objs[0].loc[0])
                            + ",17,"
                            + str(objs[0].loc[1])
                        )
                    else:
                        self.doingSafeRoute = True
                        objs = self.state.get_objects_of_type("plastic_chest")
                        if len(objs) > 0:
                            self.policy_step += 1
                            self.starting_step_safe = self.policy_step
                            return action_sets.index(
                                "TP_TO_"
                                + str(objs[0].loc[0])
                                + ",17,"
                                + str(objs[0].loc[1])
                            )
                        else:
                            self.policy_step += 1
                            return action_sets.index("NOP")
                elif self.policy_step == 27 or self.policy_step == 31:
                    vec = (0, 0)
                    if ent.facing == "NORTH":
                        vec = (-1, 0)
                    elif ent.facing == "SOUTH":
                        vec = (1, 0)
                    elif ent.facing == "WEST":
                        vec = (0, -1)
                    else:
                        vec = (0, 1)

                    new_loc = np.add(vec, ent.loc)
                    objs = self.state.get_objects_at(tuple(new_loc))
                    if len(objs[0]) > 0:
                        if objs[0][0].type != "diamond_ore":
                            self.rotate_step += 1
                            return action_sets.index("rotate_right")
                            # need to rotate until we are facing the diamond ore
                        else:
                            self.policy_step += 1
                            self.rotate_step = 0
                            return action_sets.index("NOP")
                            # do nothing as already facing the diamond ore, move onto next part of policy
                    else:
                        self.rotate_step += 1
                        return action_sets.index("rotate_right")
                        # need to rotate until we are facing the diamond ore
                elif self.policy_step == 34 or self.policy_step == 38:
                    objs = self.state.get_objects_of_type("block_of_platinum")
                    if len(objs) > 0:
                        self.policy_step += 1
                        return action_sets.index(
                            "TP_TO_"
                            + str(objs[0].loc[0])
                            + ",17,"
                            + str(objs[0].loc[1])
                        )
                    else:
                        self.policy_step += 1
                        return action_sets.index("NOP")
                elif self.policy_step == 35 or self.policy_step == 39:
                    vec = (0, 0)
                    if ent.facing == "NORTH":
                        vec = (-1, 0)
                    elif ent.facing == "SOUTH":
                        vec = (1, 0)
                    elif ent.facing == "WEST":
                        vec = (0, -1)
                    else:
                        vec = (0, 1)

                    new_loc = np.add(vec, ent.loc)
                    objs = self.state.get_objects_at(tuple(new_loc))
                    if len(objs[0]) > 0:
                        if objs[0][0].type != "block_of_platinum":
                            self.rotate_step += 1
                            return action_sets.index("rotate_right")
                            # need to rotate until we are facing the block_of_platinum
                        else:
                            self.policy_step += 1
                            self.rotate_step = 0
                            return action_sets.index("NOP")
                            # do nothing as already facing the block_of_platinum, move onto next part of policy
                    else:
                        self.rotate_step += 1
                        return action_sets.index("rotate_right")
                        # need to rotate until we are facing the block_of_platinum
                elif self.policy_step == 42:
                    self.policy_step += 1
                    return action_sets.index("TP_TO_103")
                elif self.policy_step == 43:
                    vec = (0, 0)
                    if ent.facing == "NORTH":
                        vec = (-1, 0)
                    elif ent.facing == "SOUTH":
                        vec = (1, 0)
                    elif ent.facing == "WEST":
                        vec = (0, -1)
                    else:
                        vec = (0, 1)

                    new_loc = np.add(vec, ent.loc)
                    objs = self.state.get_objects_at(tuple(new_loc))
                    if len(objs[1]) > 0:
                        if objs[1][0].type != "trader":
                            self.rotate_step += 1
                            return action_sets.index("rotate_right")
                        else:
                            self.policy_step += 1
                            self.rotate_step = 0
                            return action_sets.index("NOP")
                    else:
                        self.rotate_step += 1
                        return action_sets.index("rotate_right")
                elif self.policy_step == 44 or self.policy_step == 45:
                    self.policy_step += 1
                    return action_sets.index("trade_block_of_titanium_1")
                elif self.policy_step == 48 or self.policy_step == 49:
                    self.policy_step += 1
                    return action_sets.index("craft_block_of_diamond")
                elif self.policy_step == 50:
                    self.policy_step += 1
                    return action_sets.index("craft_pogo_stick")
                else:
                    self.policy_step = 0
                    return action_sets.index("NOP")
            else:
                # doing the safe route - now, we collect key, tp to safe, use key, and collect diamonds
                if self.policy_step == self.starting_step_safe:
                    vec = (0, 0)
                    if ent.facing == "NORTH":
                        vec = (-1, 0)
                    elif ent.facing == "SOUTH":
                        vec = (1, 0)
                    elif ent.facing == "WEST":
                        vec = (0, -1)
                    else:
                        vec = (0, 1)

                    new_loc = np.add(vec, ent.loc)
                    objs = self.state.get_objects_at(tuple(new_loc))
                    if len(objs[0]) > 0:
                        if objs[0][0].type != "plastic_chest":
                            return action_sets.index("rotate_right")
                        else:
                            self.policy_step += 1
                            return action_sets.index("NOP")
                    else:
                        return action_sets.index("rotate_right")
                elif self.policy_step == self.starting_step_safe + 1:
                    self.policy_step += 1
                    return action_sets.index("collect")
                elif self.policy_step == self.starting_step_safe + 2:
                    objs = self.state.get_objects_of_type("safe")
                    if len(objs) > 0:
                        self.policy_step += 1
                        return action_sets.index(
                            "TP_TO_"
                            + str(objs[0].loc[0])
                            + ",17,"
                            + str(objs[0].loc[1])
                        )
                    else:
                        self.policy_step += 1
                        return action_sets.index("NOP")
                elif self.policy_step == self.starting_step_safe + 3:
                    vec = (0, 0)
                    if ent.facing == "NORTH":
                        vec = (-1, 0)
                    elif ent.facing == "SOUTH":
                        vec = (1, 0)
                    elif ent.facing == "WEST":
                        vec = (0, -1)
                    else:
                        vec = (0, 1)

                    new_loc = np.add(vec, ent.loc)
                    objs = self.state.get_objects_at(tuple(new_loc))
                    if len(objs[0]) > 0:
                        if objs[0][0].type != "safe":
                            return action_sets.index("rotate_right")
                        else:
                            self.policy_step += 1
                            return action_sets.index("NOP")
                    else:
                        return action_sets.index("rotate_right")
                elif self.policy_step == self.starting_step_safe + 4:
                    self.policy_step += 1
                    return action_sets.index("use")
                elif self.policy_step == self.starting_step_safe + 5:
                    # this is where the platinum stuff starts again, done with safe route
                    self.policy_step = 34
                    self.doingSafeRoute = False
                    return action_sets.index("collect")

            # in case we don't return an action for some reason
            print("policy step: ", self.policy_step)
            return action_sets.index("NOP")
        else:  # skip every other turn
            self.isMoving = True
            action_sets = self.action_set.get_action_names()
            return action_sets.index("NOP")
