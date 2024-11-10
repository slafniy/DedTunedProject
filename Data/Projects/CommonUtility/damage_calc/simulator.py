import typing as t

from character import Character


def simulate_combat(characters: t.List[Character], rounds=5, target_ac=13) -> t.List[dict]:
    data = []
    for round_number in range(1, rounds + 1):
        for c in characters:
            round_damage = c.play_round(target_ac)
            data.append({
                'round_number': round_number,
                'spec': c.spec,
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
