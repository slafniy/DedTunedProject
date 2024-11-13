from dataclasses import dataclass

from dc_logger import dc_logger
from dice import roll_dice


@dataclass
class Weapon:
    name: str
    dice_size: int
    dice_count: int = 1
    bonus: int = 0

    def damage_roll(self, critical=False) -> int:
        """Only weapon damage, basic dice + basic enchantment, also process critical hits"""
        dice_count = self.dice_count * 2 if critical else self.dice_count
        rolls = []
        for _ in range(dice_count):
            damage = roll_dice(self.dice_size)
            # dc_logger.debug(f"\t\tDamage roll: {damage} | d{self.dice_size}")
            rolls.append(damage)
        res = sum(rolls) + self.bonus
        # dc_logger.debug(f"\t{self.name} damage: {res} | {dice_count}d{self.dice_size} + {self.bonus}{' CRITICAL' if critical else ''}")
        return res


HAND_CROSSBOW_0 = Weapon("Hand Crossbow", dice_size=6)
HAND_CROSSBOW_1 = Weapon("Hand Crossbow +1", dice_size=6, bonus=1)
HAND_CROSSBOW_2 = Weapon("Hand Crossbow +2", dice_size=6, bonus=2)

HEAVY_CROSSBOW_0 = Weapon("Heavy Crossbow", dice_size=10)
HEAVY_CROSSBOW_1 = Weapon("Heavy Crossbow +1", dice_size=10, bonus=1)
HEAVY_CROSSBOW_2 = Weapon("Heavy Crossbow +2", dice_size=10, bonus=2)

LONGBOW_0 = Weapon("Longbow", dice_size=8)
LONGBOW_1 = Weapon("Longbow +1", dice_size=8, bonus=1)
LONGBOW_2 = Weapon("Longbow +2", dice_size=8, bonus=2)
LONGBOW_3 = Weapon("Longbow +3", dice_size=8, bonus=3)


if __name__ == "__main__":
    HAND_CROSSBOW_1.damage_roll()
    HAND_CROSSBOW_1.damage_roll()
    HAND_CROSSBOW_1.damage_roll()
    HAND_CROSSBOW_1.damage_roll(True)
    HAND_CROSSBOW_1.damage_roll(True)