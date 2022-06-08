import json
import numpy as np
import random

class Map:
	def __init__(self, fileName):
		"""
		Initializes the map, a 2D numpy array, using the provided JSON
		Initializes based off of selected mode 
		Randomization gets parameters from the JSON to initialize
		entities in random locations
		Seeded initializes entities in specified coords
		"""

		self.mapper = dict()

		np.set_printoptions(threshold=np.inf)
		f = open(fileName)
		data = json.load(f)
		self.map_obj = np.zeros((data["map"]["size"], data["map"]["size"]))
		currId = 1
		for item, qt in data["map"]["objects"].items():
			for i in range(0, qt):
				row = random.randrange(0, data["map"]["size"])
				col = random.randrange(0, data["map"]["size"])
				if self.map_obj[row][col] == 0:
					self.map_obj[row][col] = currId
			self.mapper[item] = currId
			currId += 1
		print(self.map_obj)
		print(self.mapper)

	def getMap(self):
		return self.map_obj

	def getMapper(self):
		return self.mapper

if __name__ == "__main__":
	lovethelows = Map("samplemap.json")