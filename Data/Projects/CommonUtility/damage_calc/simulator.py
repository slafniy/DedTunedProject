import typing as t

from data_processing import process
from character import ProgressionBase


def simulate_combat(character_progressions: t.List[ProgressionBase],
                    target_ac_list=(13,), rounds=5, iterations=10) -> t.List[dict]:
    data = []

    for target_ac in target_ac_list:
        for progression in character_progressions:
            for iteration_number in range(iterations):
                for level in range(1, 13):
                    character = progression.get_character(level)
                    for round_number in range(1, rounds + 1):
                        data.append({
                            'iteration_number': iteration_number,
                            'round_number': round_number,
                            'name': character.name,
                            'level': character.level,
                            'target_ac': target_ac,
                            'round_damage': character.play_round(target_ac)
                        })
    df = process(data)
    return df


if __name__ == '__main__':
    import pprint
    from character import PROGRESSION_BASIC

    combat_data = simulate_combat(
        [PROGRESSION_BASIC],
        target_ac_list=(13,18),
        iterations=3
    )

    pprint.pprint(combat_data)
