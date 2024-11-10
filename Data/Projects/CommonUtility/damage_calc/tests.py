import mock

import pytest

from weapon import Weapon


@pytest.mark.parametrize('randint_value', [1, 2, 3, 4, 3, 2, 1, 4])
def test_weapon_1d4(randint_value):
    weapon = Weapon('weapon_1d4', 4, 1)

    with mock.patch('random.randint', return_value=randint_value):
        damage = weapon.damage_roll()
        assert damage == randint_value


@pytest.mark.parametrize(['randint_value_1', 'randint_value_2'], [
    [1, 2], [2, 3], [3, 6], [6, 6]
])
def test_weapon_2d6_2(randint_value_1, randint_value_2):
    weapon = Weapon('weapon_2d6+2', 6, 2, bonus=2)

    with mock.patch('random.randint', side_effect=[randint_value_1, randint_value_2]):
        damage = weapon.damage_roll()
        expected_damage = randint_value_1 + randint_value_2 + 2
        assert damage == expected_damage
