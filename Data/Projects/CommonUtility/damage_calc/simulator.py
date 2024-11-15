import typing as t
from itertools import product
from multiprocessing import Pool, cpu_count

import pandas as pd

from character import Character
from data_processing import process
from weapon import TWO_HANDED_SWORD_0


def simulate_character(character, target_ac, rounds, iterations) -> t.List[dict]:
    data = []

    while True:  # levels iteration
        # print(f">> {character.name=} {character.level=} {target_ac=}")
        for iteration_number in range(iterations):
            # do rest before each combat
            if iteration_number % 3:
                character.long_rest()
            else:
                character.short_rest()

            for round_number in range(1, rounds + 1):
                round_data = {
                    'iteration_number': iteration_number,
                    'round_number': round_number,
                    'name': character.name,
                    'level': character.level,
                    'target_ac': target_ac,
                    'round_damage': character.play_round(target_ac)
                }
                data.append(round_data)
        if not character.level_up():
            character.drop_to_level_1()
            break

    return data


# def split_iterations(iterations: int, parts=cpu_count()) -> t.List[t.Tuple[int, int]]:
#     new_size = iterations // parts
#     res = [(i, i + new_size) for i in range(0, iterations - new_size, new_size)]
#     res.append((res[-1][1], iterations))
#     return res


def simulate_combat(characters: t.List[Character], target_ac_list=(13,), rounds=15, iterations=500) -> pd.DataFrame:
    data = []

    tasks = [(character, target_ac, rounds, iterations) for character, target_ac in product(characters, target_ac_list)]

    with Pool(processes=cpu_count()) as pool:
        results = pool.starmap(simulate_character, tasks)

    for result in results:
        data += result

    df = process(data)
    return df


if __name__ == '__main__':
    import pprint
    import logging
    from character import Character
    import random

    random.seed(555)

    basic_two_handed_sword = Character("Basic 2H - no progression (only proficiency)",
                                       weapon_main=TWO_HANDED_SWORD_0,
                                       main_ability_progression={level: 17 for level in range(1, 13)})
    basic_two_handed_sword_dt_ability_progression = Character("Basic 2H - DT ability progression",
                                                              weapon_main=TWO_HANDED_SWORD_0)

    combat_data = simulate_combat(
        characters=[basic_two_handed_sword,
                    basic_two_handed_sword_dt_ability_progression],
        target_ac_list=(13, 16),
        iterations=1000,
        rounds=5
    )

    pprint.pprint(combat_data)
