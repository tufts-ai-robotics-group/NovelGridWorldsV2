import json

class Recipe:
    def __init__(self, json=None):
        #these recipes have an input of ingredients and yield and output
        #ex. 'pogo_stick': {'input': {'stick': 4, 'plank': 2, 'rubber': 1}, 'output': {'pogo_stick': 1}
        self.recipes = json

    def useFile(self, fileName):
        #takes in a fileName for a json and then parses it for the recipes
        f = open(fileName)
        self.recipes = json.load(f)


    def getRecipes(self):
        return self.recipes

    def addRecipes(self, fileName):
        #adds recipes to the current ones using a file
        f = open(fileName)
        addedRecipes = json.load(f)
        self.recipes.update(addedRecipes)

    def removeRecipe(self, toRemove):
        self.recipes.pop(toRemove)

    def recipes_to_actions(self):
        recipeNames = list(self.recipes.keys())
        print(recipeNames)
        for recipe in recipeNames:
            for item in self.recipes[recipe]["input"]:
                arda = list(item.keys())
                print(arda[0])
                print(item[arda[0]])
            for item in self.recipes[recipe]["output"]:
                arda = list(item.keys())
                print(arda[0])
                print(item[arda[0]])

        #TODO: determine action format and convert the recipes to that