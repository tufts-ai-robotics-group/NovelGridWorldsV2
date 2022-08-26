def merge_inventory(old_item, new_item):
    """
    Merges two items into one item.
    """
    for key, value in new_item.items():
        if key in old_item:
            old_item[key] += value
        else:
            old_item[key] = value
