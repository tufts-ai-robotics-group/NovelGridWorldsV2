
def collect_item(state, entity, obj, loc):
    if obj.type != "diamond_ore":
        entity.add_to_inventory(obj.type, 1)
    else:
        entity.add_to_inventory("diamond", 9)
    state.remove_object(obj.type, loc)

