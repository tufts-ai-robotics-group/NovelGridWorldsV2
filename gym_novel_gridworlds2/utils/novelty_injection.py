from copy import deepcopy


def inject(original_config, novelty) -> dict:
    """
    replaces 
    """
    copied_config = deepcopy(original_config)
    replace_item(copied_config, novelty)
    return copied_config


def replace_item(old_obj: dict, new_obj: dict, merge_list=True):
    """
    RFC7386:
    if same key exists, overwrites
    if not exist, remove.
    """
    for new_obj_k, new_obj_v in new_obj.items():
        if (
            new_obj_k in old_obj
            and isinstance(new_obj_v, dict)
            and new_obj_k in old_obj
        ):
            # new obj is a dict
            if isinstance(old_obj[new_obj_k], dict):
                # old obj also a dict, recurse and copy
                replace_item(old_obj[new_obj_k], deepcopy(new_obj[new_obj_k]))
            else:
                # new obj is a dict but old obj is non-list, deep copy and overwrite
                old_obj[new_obj_k] = deepcopy(new_obj[new_obj_k])
        else:
            # new obj is not a dict
            if new_obj_v is None:
                # new_obj is null, delete the old entry if it exists
                if new_obj_k in old_obj:
                    del old_obj[new_obj_k]
            else:
                # otherwise (might be a list), deep copy
                old_obj[new_obj_k] = deepcopy(new_obj[new_obj_k])
