import unittest
import numpy as np 

from gym_novel_gridworlds2.utils import Recipe

class RecipeTests(unittest.TestCase):
    def setUp(self):
        self.recipes = Recipe("oldrecipes.json")

    def testRecipeMod(self):
        recipe_dict = {
            "pogo_stick": {
                "input": [
                    {"stick": 4},
                    {"plank": 2},
                    {"rubber": 1}
                ],
                "output": [
                    {"pogo_stick": 1}
                ]
            },
            "stick": {
                "input": [
                    {"plank": 2}
                ],
                "output": [
                    {"stick": 4}
                ]   
            }
        }
        self.assertEqual(self.recipes.getRecipes(), recipe_dict)
        mod1_recipe_dict = {
            "pogo_stick": {
                "input": [
                    {"stick": 4},
                    {"plank": 2},
                    {"rubber": 1}
                ],
                "output": [
                    {"pogo_stick": 1}
                ]
            }
        }
        self.recipes.removeRecipe("stick")
        self.assertEqual(self.recipes.getRecipes(), mod1_recipe_dict)
        self.recipes.addRecipes("oldrecipes.json")
        self.assertEqual(self.recipes.getRecipes(), recipe_dict)


