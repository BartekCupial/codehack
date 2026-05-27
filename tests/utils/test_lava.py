import numpy as np

from codehack.utils.lava import ranked_centered_eastward_lava_bank_targets


def test_ranked_centered_eastward_lava_bank_targets_prefers_middle_of_river():
    lava_mask = np.zeros((7, 14), dtype=bool)
    lava_mask[1:6, 6] = True

    features = np.zeros((7, 14), dtype=int)
    features[1:6, 1:6] = 1
    features[1:6, 7:13] = 2

    path = [
        (3, 3),
        (2, 4),
        (1, 5),
        (1, 6),
        (1, 7),
        (2, 8),
        (3, 9),
    ]

    ranked_targets = ranked_centered_eastward_lava_bank_targets(
        path=path,
        lava_mask=lava_mask,
        features=features,
        current_position=(3, 3),
    )

    assert ranked_targets[0] == (3, 5)
    assert (1, 5) in ranked_targets
