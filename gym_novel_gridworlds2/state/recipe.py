from typing import Mapping
import warnings


class Recipe:
    def __init__(self, input_list, output_list):
        self.input_list = input_list
        self.output_list = output_list


class RecipeSet:
    def __init__(self):
        self.recipes = {}
        self.recipe_index = {}

    def add_recipe(self, recipe_name, recipe_dict):
        if isinstance(recipe_dict['input'][0]. dict):
            input_list = self.legacy_list_convert(recipe_dict['input'])
            output_list = self.legacy_list_convert(recipe_dict['output'])
            warnings.warn(
                "The Old recipe config is depreciated and will be removed at a future version.",
                DeprecationWarning)
        else:
            input_list = recipe_dict['input']
            output_list = recipe_dict['output']


        recipe = Recipe(input_list, output_list)        
        self.recipes[recipe_name] = recipe
        self.recipe_index[str(input_list)] = recipe
    
    def legacy_list_convert(self, recipe_list: Mapping[str, int]):
        new_format_list = []

        # for every item in the format of "item": 2, convert it to 
        # ["item", "item"]
        for item, count in sorted(recipe_list.values()):
            for i in range(count):
                new_format_list.append(item)
        
        # fill up all spots so the list is 9 elements long
        for i in range(9 - len(new_format_list)):
            new_format_list.append(None)
        return new_format_list


    def get_recipe(self, name):
        return self.recipes.get(name)

    def get_output_by_input(self, input_list):
        return self.recipe_index.get(str(sorted(input_list)))
