import typing as t

from character import Character
from data_processing import process
from weapon import TWO_HANDED_SWORD_0


def simulate_combat(characters: t.List[Character], target_ac_list=(13,), rounds=5, iterations=500) -> t.List[dict]:
    data = []

    for target_ac in target_ac_list:
        for character in characters:
            while True:  # levels iteration
                for iteration_number in range(iterations):
                    for round_number in range(1, rounds + 1):
                        round_data ={
                            'iteration_number': iteration_number,
                            'round_number': round_number,
                            'name': character.name,
                            'level': character.level,
                            'target_ac': target_ac,
                            'round_damage': character.play_round(target_ac)
                        }
                        data.append(round_data)
                        print(f">> {round_data}")
                if not character.level_up():
                    break
    df = process(data)
    return df


if __name__ == '__main__':
    import pprint
    import logging
    from character import Character
    import random
    random.seed(555)

    basic_two_handed_sword = Character("Basic 2H", {}, TWO_HANDED_SWORD_0,
                                       console_logging_level=logging.DEBUG)

    combat_data = simulate_combat(
        characters=[basic_two_handed_sword],
        target_ac_list=(13,),
        iterations=500,
        rounds=3
    )

    pprint.pprint(combat_data)
