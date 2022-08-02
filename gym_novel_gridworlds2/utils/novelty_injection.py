from copy import deepcopy

def inject(original_config, novelty) -> dict:
    """
    replaces 
    """
    new_config = deepcopy(original_config)
    replace_item(new_config, novelty)
    return new_config


def replace_item(old_obj: dict, new_obj: dict):
    for k, v in new_obj.items():
        if k in old_obj and isinstance(v, dict) and k in old_obj:
            replace_item(old_obj[k], new_obj[k])
        else:
            old_obj[k] = deepcopy(new_obj[k])
