from copy import deepcopy

def inject(original_config, novelty) -> dict:
    """
    replaces 
    """
    copied_config = deepcopy(original_config)
    replace_item(copied_config, novelty)
    return copied_config


def replace_item(old_obj: dict, new_obj: dict):
    for k, v in new_obj.items():
        if k in old_obj and isinstance(v, dict) and \
                k in old_obj and isinstance(old_obj[k], dict):
            replace_item(old_obj[k], deepcopy(new_obj[k]))
        else:
            old_obj[k] = deepcopy(new_obj[k])
