import logging

import mock

import pytest

from character import Character, Passive, logger
import weapon as wpn

logger.stream_handler.setLevel(logging.DEBUG)


@pytest.mark.parametrize('randint_value', [1, 2, 3, 4, 3, 2, 1, 4])
def test_weapon_1d4(randint_value):
    weapon = wpn.Weapon('weapon_1d4', 4, 1)

    with mock.patch('random.randint', return_value=randint_value):
        damage = weapon.damage_roll()
        assert damage == randint_value


@pytest.mark.parametrize(['randint_value_1', 'randint_value_2'], [
    [1, 2], [2, 3], [3, 6], [6, 6]
])
def test_weapon_2d6_2(randint_value_1, randint_value_2):
    weapon = wpn.Weapon('weapon_2d6+2', 6, 2, bonus=2)

    with mock.patch('random.randint', side_effect=[randint_value_1, randint_value_2]):
        damage = weapon.damage_roll()
        expected_damage = randint_value_1 + randint_value_2 + 2
        assert damage == expected_damage


def test_gwm_vanilla():
    gwm_on = Character("Fighter Big Sword + GWM", weapon_main=wpn.TWO_HANDED_SWORD_0,
                  passives_progression={1: {Passive.FEAT_GREAT_WEAPON_MASTER_VANILLA}})
    gwm_off = Character("Fighter Big Sword", weapon_main=wpn.TWO_HANDED_SWORD_0)

    with mock.patch('random.randint', return_value=5):
        # one attack expected, 5 + 5 sword, +3 STR and +10 from GWM, total 23
        damage = gwm_on.play_round(0)
        assert damage == 23

        # one attack expected, 5 + 5 sword, +3 STR, total 13
        damage = gwm_off.play_round(0)
        assert damage == 13

        # check roll penalty works: 5 roll +2 prof +3 STR, total 10
        # should work against AC10 and does not work against AC11
        damage = gwm_off.play_round(10)
        assert damage == 13
        damage = gwm_off.play_round(11)
        assert damage == 0

        # for gwm we should have roll -5, total 5, so expect success on AC5 and failure on AC6
        damage = gwm_on.play_round(5)
        assert damage == 23
        damage = gwm_on.play_round(6)
        assert damage == 0

    # Test critical hit bonus attack
    with mock.patch('random.randint', side_effect=[20, 3, 3, 3, 3]):
        # Expect 4d6 + STR prof, 12 + 3 = 15
        damage = gwm_off.play_round(0)
        assert damage == 15

    with mock.patch('random.randint', side_effect=[20, 3, 3, 3, 3, 3, 3, 3]):
        # Expecting 1st attack: 4d6 + STR + GWM: 12 + 3 + 10 = 25
        # and 2nd (bonus for crit) attack: 3 + 3 + 3 + 10 = 19, total damage 44
        damage = gwm_on.play_round(0)
        assert damage == 44