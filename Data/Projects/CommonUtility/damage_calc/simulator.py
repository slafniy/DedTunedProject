import typing as t

from character import Character


def simulate_combat(characters: t.List[Character], target_ac=13, rounds=5, iterations=100) -> t.List[dict]:
    data = []
    for iteration_number in range(iterations):
        for round_number in range(1, rounds + 1):
            for c in characters:
                round_damage = c.play_round(target_ac)
                data.append({
                    'iteration_number': iteration_number,
                    'round_number': round_number,
                    'name': c.name,
                    'level': c.level,
                    'round_damage': round_damage
                })
    return data




if __name__ == '__main__':
    import pprint
    from character import RANGER_LEVEL_5_DUAL, RANGER_LEVEL_5_ARCHERY

    combat_data = simulate_combat([
        RANGER_LEVEL_5_DUAL,
        RANGER_LEVEL_5_ARCHERY
    ])

    pprint.pprint(combat_data)
