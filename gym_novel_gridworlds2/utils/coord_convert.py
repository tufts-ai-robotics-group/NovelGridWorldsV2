from typing import Tuple

def internal_to_external(coord: Tuple[int, int]):
    return int(coord[1]), 17, int(coord[0])

def external_to_internal(coord: Tuple[int, int, int]):
    return coord[2], coord[0]

def internal_to_str(coord: Tuple[int, int]):
    return f"{coord[1]},17,{coord[0]}"

