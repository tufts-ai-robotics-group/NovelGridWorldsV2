def nameConversion(name):
    properties = {}
    if name == None:
        converted_name = "minecraft:air"
    elif name == "oak_log":
        converted_name = "minecraft:log"
        properties["variant"] = "oak"
    elif name == "rubber":
        converted_name = "polycraft:sack_polyisoprene_pellets"
    elif name == "block_of_titanium":
        converted_name = "polycraft:block_of_titanium"
    elif name == "block_of_platinum":
        converted_name = "polycraft:block_of_platinum"
    elif name == "diamond_ore":
        converted_name = "minecraft:diamond_ore"
    elif name == "iron_pickaxe":
        converted_name = "minecraft:iron_pickaxe"
    elif name == "block_of_diamond":
        converted_name = "minecraft:diamond_block"
    elif name == "tree_tap":
        converted_name = "polycraft:tree_tap"
    elif name == "plastic_chest":
        converted_name = "polycraft:plastic_chest"
    elif name == "pogo_stick":
        converted_name = "polycraft:wooden_pogo_stick"
    elif name == "safe":
        converted_name = "polycraft:safe"
    elif name == "unlocked_safe":
        converted_name = "polycraft:unlocked_safe"
    elif name == "bedrock":
        converted_name = "minecraft:bedrock"
    elif name == "door":
        converted_name = "minecraft:wooden_door"
    elif name == "planks":
        converted_name = "minecraft:planks"
        properties["variant"] = "oak"
    elif name == "blue_key":
        converted_name = "polycraft:key"
        properties["color"] = "blue"
    else:
        converted_name = "minecraft:" + name
    
    return converted_name, properties


def backConversion(name, variant=None, **kwargs):
    if name is None:
        return None
    res = name.split(":")
    if len(res) <= 1:
        return name

    if res[1] == "sack_polyisoprene_pellets":
        return "rubber"
    elif res[1] == "diamond_block":
        return "block_of_diamond"
    elif res[1] == "log":
        return "oak_log"
    elif res[1] == "minecraft:wooden_door":
        return "door"
    elif res[1] == "polycraft:wooden_pogo_stick":
        return "pogo_stick"
    elif res[1] == 0:
        return 0
    elif res[1] == "key":
        return kwargs.get("color", "blue") + "_key"
    else:
        return res[1]
