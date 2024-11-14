import typing as t
from itertools import product

import pandas as pd

from character import Character
from data_processing import process
from weapon import TWO_HANDED_SWORD_0


def simulate_character(character, target_ac, rounds, iterations) -> t.List[dict]:
    data = []

    while True:  # levels iteration
        print(f">> {character.name=} {character.level=} {target_ac=}")
        for iteration_number in range(iterations):
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
            break

    return data


def simulate_combat(characters: t.List[Character], target_ac_list=(13,), rounds=5, iterations=500) -> pd.DataFrame:
    data = []

    for character, target_ac in product(characters, target_ac_list):
        data += simulate_character(character, target_ac, rounds, iterations)

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
        target_ac_list=(13,),
        iterations=500,
        rounds=5
    )

    pprint.pprint(combat_data)
