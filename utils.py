from typing import List, Tuple


def load_data(
    path: str,
) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], List[List[int]]]:
    """
    Read data from file and return a tuple of size, boxPos, targetPos, tile
    """
    size = ()
    boxPos = ()
    targetPos = ()
    tile = []
    with open(path, "r") as f:
        data = f.read().splitlines()
    for idx, line in enumerate(data):
        tmp = list(map(int, line.split(" ")))
        if idx == 0 and len(tmp) == 2:
            size = tuple(tmp)
        elif idx == 1 and len(tmp) == 2:
            boxPos = tuple(tmp)
        elif idx == 2 and len(tmp) == 2:
            targetPos = tuple(tmp)
        else:
            if len(tmp) != size[1]:
                raise ValueError("Invalid data: wrong size")
            elif len(tile) < size[0]:
                tile.append(tmp)
    return size, boxPos, targetPos, tile
