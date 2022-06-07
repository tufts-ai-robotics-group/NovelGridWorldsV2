import json

class Recipe:
	def __init__(self, fileName):
		#takes in a fileName for a json and then parses it for the recipes
		#these recipes have an input of ingredients and yield and output
		#ex. 'pogo_stick': {'input': {'stick': 4, 'plank': 2, 'rubber': 1}, 'output': {'pogo_stick': 1}
		f = open(fileName)
		self.recipes = json.load(f)

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

#add modifiers 

if __name__ == "__main__":
	lovethelows = Recipe("oldrecipes.json")
	lovethelows.recipes_to_actions()
