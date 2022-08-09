def nameConversion(self, name):
    if name == None:
        return "None"
    elif name == "oak_log":
        return "minecraft:log"
    elif name == "rubber":
        return "polycraft:sack_polyisoprene_pellets"
    elif name == "block_of_titanium":
        return "polycraft:block_of_titanium"
    elif name == "block_of_platinum":
        return "polycraft:block_of_platinum"
    elif name == "diamond_ore":
        return "minecraft:diamond_ore"
    elif name == "iron_pickaxe":
        return "minecraft:iron_pickaxe"
    elif name == "block_of_diamond":
        return "minecraft:block_of_diamond"
    elif name == "tree_tap":
        return "polycraft:tree_tap"
    elif name == "plastic_chest":
        return "polycraft:plastic_chest"
    elif name == "safe":
        return "polycraft:safe"
    elif name == "bedrock":
        return "minecraft:bedrock"
    else:
        return "polycraft:" + name
