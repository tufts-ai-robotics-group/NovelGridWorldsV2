import numpy as np
from gym_novel_gridworlds2.agents.agent import Agent

class FlexiblePolicyPogoist(Agent):
    '''
    A pogoist-like agent that has a flexible policy. The policy can be specified as a series of subgoals to achieve.
    This version simply assumes all the subgoals succeed, which is fine for the pogoist.

    Subgoals are implemented as action generators. The policy looks at the current subgoal and returns its next action.
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.isMoving = False
        self.policy_step = 0
        self.rotate_step = 0
        self.before_start = 6
        self.starting_step_safe = 0
        self.doingSafeRoute = False

        #List of subgoals for this agent. TODO: specify the subgoals in the config file (use normal pogoist subgoals as default).
        self.subgoals = [self._collect_wood_subgoal(), self._go_to_obj_subgoal("crafting_table"),self._collect_wood_subgoal(),self._null_subgoal()]

        self.current_subgoal_idx = 0





    ## Convenience routines to format the actions. Prevents repetition.
    def _goto_action(self,obj):
        action_sets = self.action_set.get_action_names()
        return action_sets.index("TP_TO"), {
            "x": obj.loc[0],
            "z": 17,
            "y": obj.loc[1],
        }
    def _rotate_action(self):
        action_sets = self.action_set.get_action_names()
        return action_sets.index("rotate_right")

    def _get_obj_infront(self):
        ent = self.state.get_entity_by_id(105) # what is this magic number? Is this me? I should probably know my id
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
        return objs


    def _null_subgoal(self):
        '''
        Null subgoal whose actions are always NOP. Can use at the end of the policy to just have the agent.
        '''
        while True:
            #always NOP
            yield self.action_set.get_action_names().index("NOP")

    def _go_to_obj_subgoal(self,obj_type):
        '''
        Slightly more interesting subgoal to go to an object. Waits for the object to exist before going.
        '''
        action_sets = self.action_set.get_action_names()
        objs = self.state.get_objects_of_type(obj_type)
        while len(objs) == 0:
            yield action_sets.index("NOP")
            objs = self.state.get_objects_of_type(obj_type)

        yield self._goto_action(objs[0])




    def _collect_wood_subgoal(self):
        '''
        A subgoal with multple steps.  The subgoal is a generator -- read up on generators if not familiar.
        The main idea is that the function "pauses" and returns whatever follows the 'yield' keyword. When the function is called again, it resumes from that point.
        So a subgoal is a generator of actions.

        This is a subgoal to collect one piece of oak_log. The steps
            1. Go to the nearest tree
            2. Face tree
            3. Break tree
            4. Collect oak_log

        Note that we can package up multiple subgoals into a single generator to make subpolicies. A subpolicy could be to collect X pieces of an object by collecting one X times.

        '''
        action_sets = self.action_set.get_action_names()
        ent = self.state.get_entity_by_id(105)
        initial_wood_amount = ent.inventory.get("oak_log",0)
        objs = self.state.get_objects_of_type("oak_log")

        while len(objs) == 0: # wait for wood to be available
            yield action_sets.index("NOP")
            objs = self.state.get_objects_of_type("oak_log")

        # go to wood
        yield self._goto_action(objs[0])

        #Look at wood
        obj_infront = self._get_obj_infront()
        is_oak_log = obj_infront[0][0].type == "oak_log" if len(obj_infront[0]) > 0 else False

        while not is_oak_log: # while not facing wood, rotate
            yield self._rotate_action()
            #Remember, the function resume from here so need to refresh these variables -- otherwise infinite loop
            obj_infront = self._get_obj_infront()
            is_oak_log = obj_infront[0][0].type == "oak_log" if len(obj_infront[0]) > 0 else False


        #If you get here, you have wood infront of you, so collect it
        yield action_sets.index("break_block")

        #collect by taking one step forward
        yield action_sets.index("smooth_move")

        #now this subgoal is done.


    def policy(self, observation):
        """
        Here a policy just looks at the current subgoal and returns its next action.
        If the subgoal is done, advance to the next subgoal.
        """

        action_sets = self.action_set.get_action_names()

        if not self.isMoving: #guard statement is preferable to multiple nesting levels
            self.isMoving = True
            return action_sets.index("NOP")

        try:
            action = next(self.subgoals[self.current_subgoal_idx])
        except StopIteration: #if subgoal done
            self.current_subgoal_idx +=1
            if self.current_subgoal_idx == len(self.subgoals): #if no more subgoals
                action = action_sets.index("NOP") # this could be different, maybe loop back to the beginning? (would need to reset generators)
            else:
                action = next(self.subgoals[self.current_subgoal_idx])
        self.policy_step += 1
        return action
