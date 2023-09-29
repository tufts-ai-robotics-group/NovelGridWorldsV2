from copy import deepcopy
import re

def inject(original_config, novelty) -> dict:
    """
    replaces 
    """
    copied_config = deepcopy(original_config)
    replace_item(copied_config, novelty)
    return copied_config

def test_merge_list():
    list_a = ["a", "b", "c"]
    list_b = ["->   123", "+d", "c -> e", "b -> "]
    merge_lists(list_a, list_b)
    # print(list_a)
    assert(list_a == ["a", "", "e", "d"])

def merge_lists(base_list: list, new_list: list):
    for item in new_list:
        if "->" in item:
            old_key, new_key = re.split(r"\s*->\s*", item)
            try:
                # replace the key
                idx = base_list.index(old_key)
                base_list[idx] = new_key
            except ValueError:
                # ignore the key
                pass
        elif len(item) > 0 and item[0] == "+":
            base_list.append(item.lstrip("+ "))


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
        elif new_obj_v is None:
            # new_obj is null, delete the old entry if it exists
            if new_obj_k in old_obj:
                del old_obj[new_obj_k]
        elif type(new_obj_v) == list and len(new_obj_v) > 0 and \
                new_obj_k in old_obj and type(old_obj[new_obj_k]) == list and \
                ("->" in new_obj_v[0] or "+" in new_obj_v[0]):
            # new object is list, but we have a special syntax for list.
            # criterion is that the old list must have the same list under the same key
            # and the new list must contain strs and the first entry
            # must contain a special character.
            # Syntax:
            # old_name -> new_name is the syntax of replacing an entry in the 
            #      list with a new one. 
            # + new_obj is the syntax of adding objects.
            # only check the first we require substitute actions to be the first.
            print('merge')
            merge_lists( old_obj[new_obj_k], new_obj_v)
        else:
            # otherwise (might be a list), deep copy
            old_obj[new_obj_k] = deepcopy(new_obj[new_obj_k])

if __name__ == "__main__":
    test_merge_list()
