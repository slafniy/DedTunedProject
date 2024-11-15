import logging

import mock

import pytest

from character import Character, Passive, logger
import weapon as wpn
from resource import Resource, ReplenishType

logger.stream_handler.setLevel(logging.DEBUG)


@pytest.mark.parametrize('randint_value', [1, 2, 3, 4, 3, 2, 1, 4])
def test_weapon_1d4(randint_value):
    weapon = wpn.Weapon('weapon_1d4', 4, 1)
    c = Character("test", weapon)
    with mock.patch('random.randint', return_value=randint_value):
        damage = c.damage_roll(weapon)
        assert damage == randint_value


@pytest.mark.parametrize(['randint_value_1', 'randint_value_2'], [
    [1, 2], [2, 3], [3, 6], [6, 6]
])
def test_weapon_2d6_2(randint_value_1, randint_value_2):
    weapon = wpn.Weapon('weapon_2d6+2', 6, 2, bonus=2)
    c = Character("test", weapon)
    with mock.patch('random.randint', side_effect=[randint_value_1, randint_value_2]):
        damage = c.damage_roll(weapon)
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


def test_reckless_attack():
    reckless_attack_off = Character("Barb Big Axe", weapon_main=wpn.TWO_HANDED_AXE_0)
    reckless_attack_on = Character("Barb Big Axe Reckless", weapon_main=wpn.TWO_HANDED_AXE_0,
                                   passives_progression={1: {Passive.PASSIVE_RECKLESS_ATTACK}})
    # Attack roll bonus: +2 proficiency, +3 STR
    with mock.patch('random.randint', return_value=5):
        # Expect attack roll 2 + 3 + 5 = 10, damage 5 + 3 = 8
        damage = reckless_attack_off.play_round(10)
        assert damage == 8
        # Expect miss
        damage = reckless_attack_off.play_round(11)
        assert damage == 0

    with mock.patch('random.randint', side_effect=[5, 1, 5]):
        # Expect attack roll 10, damage 8
        damage = reckless_attack_on.play_round(10)
        assert damage == 8

    with mock.patch('random.randint', side_effect=[5, 6, 5]):
        # Expect 1st attack roll 10, 2nd attack roll (re-roll) 11, damage 8
        damage = reckless_attack_on.play_round(11)
        assert damage == 8


@pytest.mark.parametrize(['character', 'rolls', 'expected_damage'], [
    # no GWF

    # [Character("gwf_off", wpn.TWO_HANDED_AXE_0), [5, 3], 6],

    # [Character("gwf_off", wpn.TWO_HANDED_AXE_0), [5, 2], 5],
    # [Character("gwf_off", wpn.TWO_HANDED_AXE_0), [5, 1], 4],
    # GWF bug roll > 2
    [Character("gwf_on", wpn.TWO_HANDED_AXE_0,
               passives_progression={1: {Passive.FIGHTING_STYLE_GREAT_WEAPON_FIGHTING}}), [5, 3], 6],
    # GWF re-roll 1 and 2 to 10
    # [Character("gwf_on", wpn.TWO_HANDED_AXE_0,
    #            passives_progression={1: {Passive.FIGHTING_STYLE_GREAT_WEAPON_FIGHTING}}), [5, 2, 10], 13],
    # [Character("gwf_on", wpn.TWO_HANDED_AXE_0,
    #            passives_progression={1: {Passive.FIGHTING_STYLE_GREAT_WEAPON_FIGHTING}}), [5, 1, 10], 13],
    # GWF re-roll 1 into 2
    # [Character("gwf_on", wpn.TWO_HANDED_AXE_0,
    #            passives_progression={1: {Passive.FIGHTING_STYLE_GREAT_WEAPON_FIGHTING}}), [5, 1, 2], 5]
])
def test_great_weapon_fighting(character, rolls, expected_damage):
    with mock.patch('random.randint', side_effect=rolls):
        damage = character.play_round(0)
        assert damage == expected_damage


def test_action_surge():
    passives_progression = {5: {Passive.PASSIVE_EXTRA_ATTACK},
                            11: {Passive.PASSIVE_SECOND_EXTRA_ATTACK}}
    resource_progression = {2: {Resource("ActionSurge", ReplenishType.SHORT_REST, 1)}}
    character = Character("ActionSurgeChar", weapon_main=wpn.TWO_HANDED_AXE_0,
                          passives_progression=passives_progression,
                          resource_progression=resource_progression)
    # On level 1 should not have AS
    # 1 attack 5 + 3 STR = 8 damage
    with mock.patch('random.randint', return_value=5):
        damage = character.play_round(0)
        assert damage == 8

    character.level_up(1)  # get level 2

    # Should have 1 charge of ActionSurge,
    # 2 attacks, 16 damage
    with mock.patch('random.randint', return_value=5):
        damage = character.play_round(0)
        assert damage == 16
        # and next round singe attack because there is no action surge charge
        damage = character.play_round(0)
        assert damage == 8

    character.level_up(3)  # get level 5

    # should have 4 attacks here, 4x8 damage
    with mock.patch('random.randint', return_value=5):
        damage = character.play_round(0)
        assert damage == 32
        # next round only 2 attacks
        damage = character.play_round(0)
        assert damage == 16

    character.level_up(6)  # get level 11

    # expect 6 x (5 + 5 STR) damage
    with mock.patch('random.randint', return_value=5):
        damage = character.play_round(0)
        assert damage == 60
        # next round only 3 attacks
        damage = character.play_round(0)
        assert damage == 30


def test_savage_attacker():
    no_sa = Character("no_SA", weapon_main=wpn.TWO_HANDED_SWORD_0)

    # damage roll 5 + 5 + 3 STR
    with mock.patch('random.randint', side_effect=[5, 5, 5]):
        damage = no_sa.play_round(0)
        assert damage == 13

    has_sa = Character("has_SA", weapon_main=wpn.TWO_HANDED_SWORD_0,
                       passives_progression={1: {Passive.FEAT_SAVAGE_ATTACKER}})
    # damage roll max(5,3) + max(2,4) + 3 STR
    with mock.patch('random.randint', side_effect=[5, 5, 3, 2, 4]):
        damage = has_sa.play_round(0)
        assert damage == 12

    has_sa_gwf = Character("has_SA_GWF", weapon_main=wpn.TWO_HANDED_AXE_0,
                           passives_progression={1: {Passive.FEAT_SAVAGE_ATTACKER,
                                                     Passive.FIGHTING_STYLE_GREAT_WEAPON_FIGHTING}})
    # expected damage: 1 - GWF reroll to 3, 1 - SA reroll to 2
    # max(3,2) from SA -> 3 + 3 STR = 6 total
    with mock.patch('random.randint', side_effect=[5, 1, 3, 1, 2]):
        damage = has_sa_gwf.play_round(0)
        assert damage == 6

    # expected: 2 reroll to 3, 4 not rerolled, max(3,4) + 3
    with mock.patch('random.randint', side_effect=[5, 2, 3, 4, 5]):
        damage = has_sa_gwf.play_round(0)
        assert damage == 7

    has_sa_gwf_sword = Character("has_SA_GWF_SWORD", weapon_main=wpn.TWO_HANDED_SWORD_0,
                                 passives_progression={1: {Passive.FEAT_SAVAGE_ATTACKER,
                                                           Passive.FIGHTING_STYLE_GREAT_WEAPON_FIGHTING}})
    with mock.patch('random.randint', side_effect=
    [5,  # attack roll
     2, 4, 5, # SA rolls: (roll, GWF reroll) + roll2 -> 5
     6, 1, 4  # SA rolls: roll1 + (roll, GWF reroll) -> 6
     ]):
        damage = has_sa_gwf_sword.play_round(0)
        assert damage == 14
