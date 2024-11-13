import typing as t

from data_processing import process
from character import Character


def simulate_combat(character_progressions: t.List[t.Dict[int, Character]],
                    target_ac_list=(13,), rounds=5, iterations=10) -> t.List[dict]:
    data = []

    for target_ac in target_ac_list:
        for progression in character_progressions:
            for iteration_number in range(iterations):
                character = progression[1]  # should always have level 1 character defined
                for level in range(1, 13):
                    for round_number in range(1, rounds + 1):
                        character = progression.get(level, character)  # update character if needed
                        character.level = level  # Update level to update level-related stats

                        round_damage = character.play_round(target_ac)
                        data.append({
                            'iteration_number': iteration_number,
                            'round_number': round_number,
                            'name': character.name,
                            'level': character.level,
                            'target_ac': target_ac,
                            'round_damage': round_damage
                        })
    df = process(data)
    return df


if __name__ == '__main__':
    import pprint
    from character import TWO_HANDED_SWORD_GREAT_WEAPON_FIGHTING_GWM_VANILLA

    combat_data = simulate_combat(
        [TWO_HANDED_SWORD_GREAT_WEAPON_FIGHTING_GWM_VANILLA],
        target_ac_list=(13,18),
        iterations=3
    )

    pprint.pprint(combat_data)
