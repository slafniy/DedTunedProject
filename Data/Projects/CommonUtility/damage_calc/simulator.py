import typing as t

from character import Character
from data_processing import process
from weapon import TWO_HANDED_SWORD_0


def simulate_combat(characters: t.List[Character], target_ac_list=(13,), rounds=5, iterations=1) -> t.List[dict]:
    data = []

    for target_ac in target_ac_list:
        for character in characters:
            for iteration_number in range(iterations):
                while True:
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
                    if character.level > 1:
                        break
    df = process(data)
    return df


if __name__ == '__main__':
    import pprint
    from character import Character

    basic_two_handed_sword = Character("Basic 2H", {}, TWO_HANDED_SWORD_0)

    combat_data = simulate_combat(
        characters=[basic_two_handed_sword],
        target_ac_list=(13,),
        iterations=3
    )

    pprint.pprint(combat_data)
