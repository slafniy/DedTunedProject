import typing as t

from character import Character


def simulate_combat(character_progressions: t.List[t.Dict[int, Character]],
                    target_ac=13, rounds=5, iterations=10) -> t.List[dict]:
    data = []
    for iteration_number in range(iterations):
        for progression in character_progressions:
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
                        'round_damage': round_damage
                    })
    return data


if __name__ == '__main__':
    import pprint
    from character import ALL_PROGRESSIONS

    combat_data = simulate_combat(
        ALL_PROGRESSIONS,
        target_ac=13,
        iterations=100
    )

    pprint.pprint(combat_data)
