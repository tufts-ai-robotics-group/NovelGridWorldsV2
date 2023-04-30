from typing import Type, List, Mapping

from gym_novel_gridworlds2.contrib.polycraft.objects.polycraft_obj import PolycraftObject
from gym_novel_gridworlds2.contrib.polycraft.states import PolycraftState


def generate_item_around(
        state: PolycraftState, 
        obj_class_map: Mapping[str, Type[PolycraftObject]],
        center_obj_name: str, 
        new_obj_name: str, 
        new_obj_attr: dict = {},
        radius: int=1, 
        replace=False, 
        **kwargs
    ):
    """
    Generate a new object around a center object. returns all generated objects.

    TODO replace functionality not tested. want to add room functionality
    """
    obj_info = obj_class_map[new_obj_name]
    NewObjClass = obj_info['module']
    new_obj_attr = {**obj_info['params'], **new_obj_attr}
    # find the object
    objs: List[PolycraftObject] = state.get_objects_of_type(center_obj_name)
    generated_objs = []
    for obj in objs:
        for x in range(obj.loc[0] - radius, obj.loc[0] + radius + 1):
            for y in range(obj.loc[1] - radius, obj.loc[1] + radius + 1):
                if x < 0 or y < 0 or x > state._map.shape[0] or y > state._map.shape[1]:
                    # out of map
                    continue
                elif state.get_object_at((x, y)) is not None:
                    if replace:
                        # replace object if there's anything surrounding it
                        obj: PolycraftObject = state.get_object_at((x, y))
                        if obj.type == new_obj_name or obj.type == "bedrock" or obj.type == center_obj_name:
                            # do not replace bedrock or center object
                            continue
                        else:
                            state.remove_object(obj.type, (x, y))
                    else:
                        # should not replace existing obj
                        continue
                generated_objs.append(
                    state.place_object(new_obj_name, NewObjClass, {"loc": (x, y), **new_obj_attr})
                )
    return generated_objs
