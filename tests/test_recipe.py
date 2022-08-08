import unittest
import numpy as np 
import gym

# from gym_novel_gridworlds2.utils import Recipe
# from gym_novel_gridworlds2.envs.gym_novel_gridworlds2 import NovelGridWorldEnv

# class RecipeTests(unittest.TestCase):

#     def testRecipeFileMod(self):
#         self.recipes = Recipe()
#         self.recipes.useFile("oldrecipes.json")
#         recipe_dict = {
#             "pogo_stick": {
#                 "input": [
#                     {"stick": 4},
#                     {"plank": 2},
#                     {"rubber": 1}
#                 ],
#                 "output": [
#                     {"pogo_stick": 1}
#                 ]
#             },
#             "stick": {
#                 "input": [
#                     {"plank": 2}
#                 ],
#                 "output": [
#                     {"stick": 4}
#                 ]   
#             }
#         }
#         self.assertEqual(self.recipes.getRecipes(), recipe_dict)
#         mod1_recipe_dict = {
#             "pogo_stick": {
#                 "input": [
#                     {"stick": 4},
#                     {"plank": 2},
#                     {"rubber": 1}
#                 ],
#                 "output": [
#                     {"pogo_stick": 1}
#                 ]
#             }
#         }
#         self.recipes.removeRecipe("stick")
#         self.assertEqual(self.recipes.getRecipes(), mod1_recipe_dict)
#         self.recipes.addRecipes("oldrecipes.json")
#         self.assertEqual(self.recipes.getRecipes(), recipe_dict)

#     def testRecipeMod(self):
#         recipe_dict = {
#             "pogo_stick": {
#                 "input": [
#                     {"stick": 4},
#                     {"plank": 2},
#                     {"rubber": 1}
#                 ],
#                 "output": [
#                     {"pogo_stick": 1}
#                 ]
#             },
#             "stick": {
#                 "input": [
#                     {"plank": 2}
#                 ],
#                 "output": [
#                     {"stick": 4}
#                 ]   
#             }
#         }
#         self.recipes = Recipe(recipe_dict)
#         self.assertEqual(self.recipes.getRecipes(), recipe_dict)
#         mod1_recipe_dict = {
#             "pogo_stick": {
#                 "input": [
#                     {"stick": 4},
#                     {"plank": 2},
#                     {"rubber": 1}
#                 ],
#                 "output": [
#                     {"pogo_stick": 1}
#                 ]
#             }
#         }
#         self.recipes.removeRecipe("stick")
#         self.assertEqual(self.recipes.getRecipes(), mod1_recipe_dict)
#         self.recipes.addRecipes("oldrecipes.json")
#         self.assertEqual(self.recipes.getRecipes(), recipe_dict)


