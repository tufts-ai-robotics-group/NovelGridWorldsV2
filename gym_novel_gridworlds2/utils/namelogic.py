def nameConversion(name):
    if name == None:
        return "minecraft:air"
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
        return "minecraft:diamond_block"
    elif name == "tree_tap":
        return "polycraft:tree_tap"
    elif name == "plastic_chest":
        return "polycraft:plastic_chest"
    elif name == "pogo_stick":
        return "polycraft:wooden_pogo_stick"
    elif name == "safe":
        return "polycraft:safe"
    elif name == "bedrock":
        return "minecraft:bedrock"
    elif name == "door":
        return "minecraft:wooden_door"
    else:
        return "minecraft:" + name


def backConversion(name):
    res = name.split(":")
    if (len(res) <= 1):
        return name
    
    if res[1] == "sack_polyisoprene_pellets":
        return "rubber"
    elif res[1] == "log":
        return "oak_log"
    elif res[1] == "minecraft:wooden_door":
        return "door"
    elif res[1] == "polycraft:wooden_pogo_stick":
        return "pogo_stick"
    elif res[1] == 0:
        return 0
    else:
        return res[1]
