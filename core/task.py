import pathlib
from typing import Literal, Union

import numpy as np

try:
    from ....reward_classes import BaseReward
    from ....utils import check_seed
    from ...yaml_tools import load_task_from_yaml
except ImportError:
    from rewardgym import check_seed
    from rewardgym.reward_classes import BaseReward
    from rewardgym.tasks.yaml_tools import load_task_from_yaml


def get_task(
    render_backend: Literal["pygame", "psychopy"] = None,
    seed: Union[int, np.random.Generator] = 1000,
    key_dict=None,
    **kwargs,
):
    seed = check_seed(seed)
    yaml_file = pathlib.Path(__file__).parents[1].resolve() / "task.yaml"
    info_dict, environment_graph = load_task_from_yaml(yaml_file)

    reward_structure = {
        6: BaseReward(-5),
        7: BaseReward(-1),
        8: BaseReward(0),
        9: BaseReward(1),
        10: BaseReward(5),
    }

    info_dict.update(
        {
            "position": {
                0: "large-loss",
                1: "small-loss",
                2: "neutral",
                3: "small-win",
                4: "large-win",
            }
        }
    )

    action_map = {}

    if render_backend == "pygame":
        from .backend_pygame import get_pygame_info

        pygame_dict = get_pygame_info(action_map)
        info_dict.update(pygame_dict)

    elif render_backend == "psychopy" or render_backend == "psychopy-simulate":
        from .backend_psychopy import get_psychopy_info

        if key_dict is None:
            key_dict = {"left": 0, "right": 1}

        psychopy_dict, _ = get_psychopy_info(
            seed=seed, key_dict=key_dict, fullpoints=info_dict["meta"]["fullpoints"]
        )
        info_dict.update(psychopy_dict)

    return environment_graph, reward_structure, info_dict
