import random
from constants import ATTACK_ROLL_DICE_SIZE


def roll_dice(dice_size=ATTACK_ROLL_DICE_SIZE) -> int:
    return random.randint(1, dice_size)


def dice_avg(dice_size) -> float:
    return (dice_size + 1) / 2.0


def base_weapon_damage_avg(dice_size, dice_count=1, bonus=0) -> float:
    return (dice_avg(dice_size) + bonus) * dice_count
