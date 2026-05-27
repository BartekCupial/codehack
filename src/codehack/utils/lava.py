import numpy as np


def _lava_component_from(start, lava_mask):
    height, width = lava_mask.shape
    stack = [start]
    seen = {start}
    component = []

    while stack:
        y, x = stack.pop()
        component.append((y, x))

        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny = y + dy
            nx = x + dx
            neighbor = (ny, nx)
            if 0 <= ny < height and 0 <= nx < width and lava_mask[neighbor] and neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)

    return component


def ranked_centered_eastward_lava_bank_targets(path, lava_mask, features, current_position):
    """
    Rank west-bank approach tiles for the lava component crossed by ``path``.

    The freezing strategies currently fire eastward, so we only consider lava
    boundary tiles whose west neighbor belongs to the bot's current feature.
    Candidates are ranked by how close their adjacent lava tile is to the
    center of that west-facing lava boundary.
    """

    if not path:
        return []

    path = [tuple(point) for point in path]
    first_lava = next((point for point in path if lava_mask[point]), None)
    if first_lava is None:
        return []

    current_feature = features[current_position]
    if current_feature == 0:
        return []

    height, width = lava_mask.shape
    river_tiles = _lava_component_from(first_lava, lava_mask)
    boundary_tiles = []
    for lava_y, lava_x in river_tiles:
        bank_x = lava_x - 1
        if bank_x < 0 or bank_x >= width:
            continue

        bank_tile = (int(lava_y), int(bank_x))
        if features[bank_tile] == current_feature:
            boundary_tiles.append(((int(lava_y), int(lava_x)), bank_tile))

    if not boundary_tiles:
        return []

    center = np.mean([lava_tile for lava_tile, _ in boundary_tiles], axis=0)

    def sort_key(candidate):
        lava_tile, bank_tile = candidate
        lava_dist = np.sum((np.asarray(lava_tile, dtype=float) - center) ** 2)
        path_dist = abs(lava_tile[0] - first_lava[0]) + abs(lava_tile[1] - first_lava[1])
        return lava_dist, path_dist, bank_tile[0], bank_tile[1]

    ranked_targets = []
    seen = set()
    for _, bank_tile in sorted(boundary_tiles, key=sort_key):
        if bank_tile not in seen:
            ranked_targets.append(bank_tile)
            seen.add(bank_tile)

    return ranked_targets
