import numpy as np
from gym_novel_gridworlds2.agents.agent import Agent
import re

class FlexiblePolicyPogoist(Agent):
    '''
    A pogoist-like agent that has a flexible policy. The policy can be specified as a series of subgoals to achieve.
    This version simply assumes all the subgoals succeed, which is fine for the pogoist.

    Subgoals are implemented as action generators. The policy looks at the current subgoal and returns its next action.
    '''

    def __init__(self, plan = None,**kwargs):
        super().__init__(**kwargs)
        self.isMoving = False
        self.policy_step = 0
        self.rotate_step = 0
        self.before_start = 6
        self.starting_step_safe = 0
        self.doingSafeRoute = False
        
        
        if plan is None:
            #default pogoist plan
            plan = ["collect(oak_log,None)","collect(oak_log,None)","collect(oak_log,None)","goto(crafting_table)","face(crafting_table)","craft(tree_tap)",
                    "goto(oak_log)","face(oak_log)","use_tree_tap()","collect(diamond_ore,iron_pickaxe)",
                    "collect(diamond_ore,iron_pickaxe)","collect(block_of_platinum,iron_pickaxe)","collect(block_of_platinum,iron_pickaxe)","trade(block_of_titanium_1,103,2)",
                    "goto(crafting_table)","face(crafting_table)","craft(block_of_diamond)","craft(block_of_diamond)","craft(pogostick)","nop()"]

        #Need to map plan to functions
        self.subgoals = list(map(self._plan_item_to_subgoal,plan))

        self.current_subgoal_idx = 0

    def _plan_item_to_subgoal(self,plan_item):
        
        args = re.findall('\(.*\)',plan_item)[0].strip("()").split(",")
        args = [i if i!='None' else None for i in args]

        name = plan_item.split("(")[0]
        if name== 'collect':
            return self._collect_resource_subgoal(args[0],args[1])

        if name=='goto':
            return self._go_to_obj_subgoal(args[0])   
        
        if name=='nop':
            return self._null_subgoal()
        if name=='craft':
            return self._craft_item_subgoal(args[0])

        if name=='use_tree_tap':
            return self._use_treetap_subgoal()
        if name=='face':
            return self._face_subgoal(args[0])

        if name=='trade':
            return self._trade_subgoal(args[0],args[1],int(args[2]))

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

    def _noop_action(self):
        '''
        No-op action.
        '''
        action_sets = self.action_set.get_action_names()
        return action_sets.index("NOP")

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


    def _craft_item_subgoal(self,item):
        '''
        This should yield the action necessary to craft item. hardcoding treetap for demonstration purposes, but it should:
        1. Retrieve the recipe for the selected item
        2. If a resource required to craft `item` not in inventory, try to craft it. This could be recursive to accomodate deeper crafting trees. 
        3. Craft item
        '''
        action_sets = self.action_set.get_action_names()
        #TODO: Generalize this function to use the recipes to create the list of crafting steps. 
        if item =='tree_tap':
            steps =  self._craft_treetap_steps()
        elif item == 'block_of_diamond':
            steps = [action_sets.index("craft_block_of_diamond")]
        elif item == 'pogostick':
            steps = [action_sets.index("craft_pogo_stick")]
        else:
            raise NotImplementedError(f"Crafting subgoal for {item} not implemented")

        for step in steps:
            yield step



    def _craft_treetap_steps(self):
        '''
        This is a hack. The list of steps should come from recipes
        '''
        action_sets = self.action_set.get_action_names()
        steps = [
        action_sets.index("craft_planks"),
        action_sets.index("craft_planks"),
        action_sets.index("craft_planks"),
        action_sets.index("craft_stick"),
        action_sets.index("craft_tree_tap")
        ]
        return steps


    def _use_treetap_subgoal(self):
        '''
        Specific subgoal to use the tree tap. 
        '''
        ent = self.state.get_entity_by_id(105)
        action_sets = self.action_set.get_action_names()
    
        yield action_sets.index("smooth_move"),{"direction":'x'}
        yield action_sets.index("select_tree_tap")
        yield action_sets.index("place")
        yield action_sets.index("collect")

    def _face_subgoal(self,obj):
        obj_infront = self._get_obj_infront()
        is_obj = obj_infront[0][0].type == obj if len(obj_infront[0]) > 0 else False
        is_ent = obj_infront[1][0].type == obj if len(obj_infront[1]) > 0 else False
        while not is_obj and not is_ent: # while not facing obj or entity, rotate
            yield self._rotate_action()
            #Remember, the function resume from here so need to refresh these variables -- otherwise infinite loop
            obj_infront = self._get_obj_infront()
            is_obj = obj_infront[0][0].type == obj if len(obj_infront[0]) > 0 else False
            is_ent = obj_infront[1][0].type == obj if len(obj_infront[1]) > 0 else False
        else:
            yield self._noop_action()

    def _trade_subgoal(self,trade_name,trader_id='103',repeats=1):
        '''
        Subgoal to trade an item.
        '''
        action_sets = self.action_set.get_action_names()
        
        yield action_sets.index(f"TP_TO_{trader_id}")

        face_sub = self._face_subgoal('trader')
        for i in range(4):
            try:
                yield next(face_sub)
            except StopIteration:
                break
        for _ in range(repeats):
            yield action_sets.index(f"trade_{trade_name}")
        

            

        

    def _collect_resource_subgoal(self, resource = 'oak_log', break_tool = None):
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
        initial_amount = ent.inventory.get(resource,0)
        objs = self.state.get_objects_of_type(resource)

        while len(objs) == 0: # wait for resource to be available
            yield action_sets.index("NOP")
            objs = self.state.get_objects_of_type(resource)

        # go to wood
        yield self._goto_action(objs[0])

        #Look at wood
        obj_infront = self._get_obj_infront()
        is_oak_log = obj_infront[0][0].type == resource if len(obj_infront[0]) > 0 else False
        
        face_resource_subgoal = self._face_subgoal(resource)

        for i in range(4):
            try:
                yield next(face_resource_subgoal)
            except StopIteration:
                break
        
        # use tool if necessary
        if break_tool is not None:
            yield action_sets.index(f"select_{break_tool}")
        

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
            self.current_subgoal_idx += 1
            if self.current_subgoal_idx == len(self.subgoals): #if no more subgoals
                action = action_sets.index("NOP") # this could be different, maybe loop back to the beginning? (would need to reset generators)
            else:
                action = next(self.subgoals[self.current_subgoal_idx])
        self.policy_step += 1
        self.isMoving = False
        return action
