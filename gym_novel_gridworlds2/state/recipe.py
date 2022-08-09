from typing import Iterable, List, Mapping, Optional
import warnings


class Recipe:
    def __init__(self, input_list, output_list, step_cost=None):
        self.input_list = input_list
        self.output_list = output_list
        self.step_cost = step_cost

        # compute an input dict
        self.input_dict = {}
        for item in input_list:
            if item not in self.input_dict:
                self.input_dict[item] = 1
            else:
                self.input_dict[item] += 1


class RecipeSet:
    def __init__(self, default_step_cost: Optional[int] = 1000):
        self.recipes: Mapping[str, Recipe] = {}
        self.recipe_index: Mapping[str, Recipe] = {}
        self.default_step_cost = default_step_cost

    def add_recipe(self, recipe_name, recipe_dict):
        if isinstance(recipe_dict['input'][0], dict):
            input_list = self.legacy_list_convert(recipe_dict['input'])
            output_list = self.legacy_list_convert(recipe_dict['output'])
            warnings.warn(
                "The Old recipe config is depreciated and will be removed at a future version.",
                DeprecationWarning)
        else:
            input_list = recipe_dict['input']
            output_list = recipe_dict['output']
        
        step_cost = recipe_dict.get('step_cost')
        if step_cost is None:
            step_cost = self.default_step_cost
        recipe = Recipe(input_list, output_list, step_cost)        
        self.recipes[recipe_name] = recipe
        self.recipe_index[self.list_to_recipe_index(input_list)] = recipe
    
    def legacy_list_convert(self, recipe_list: List[Mapping[str, int]]):
        new_format_list = []

        # for every item in the format of "item": 2, convert it to 
        # ["item", "item"]
        tuple_list = []
        for entry in recipe_list:
            for item, count in entry.items():
                tuple_list.append((item, count))

        for item, count in sorted(tuple_list):
            for i in range(count):
                new_format_list.append(item)
        
        # fill up all spots so the list is either 4 or 9 elements long
        if len(new_format_list) <= 4:
            recipe_len = 4
        else:
            recipe_len = 9
        for i in range(recipe_len - len(new_format_list)):
            new_format_list.append("0")
        return new_format_list


    def get_recipe(self, name) -> Optional[Recipe]:
        return self.recipes.get(name)

    def list_to_recipe_index(self, input_list):
        return "~".join(sorted(filter(lambda o: o is not None, input_list)))

    def get_recipe_by_input(self, input_list):
        if not isinstance(input_list, Iterable):
            return None
        index_key = self.list_to_recipe_index(list(input_list))
        return self.recipe_index.get(index_key)
    
    def get_recipe_names(self):
        return self.recipes.keys()
