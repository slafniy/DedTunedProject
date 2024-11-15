from dataclasses import dataclass


@dataclass
class Weapon:
    name: str
    dice_size: int
    dice_count: int = 1
    bonus: int = 0


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

SHORT_SWORD_0 = Weapon("Short Sword", dice_size=6)
SHORT_SWORD_1 = Weapon("Short Sword +1", dice_size=6, bonus=1)
SHORT_SWORD_2 = Weapon("Short Sword +2", dice_size=6, bonus=2)

TWO_HANDED_SWORD_0 = Weapon("Two Handed Sword", dice_size=6, dice_count=2)
TWO_HANDED_SWORD_1 = Weapon("Two Handed Sword +1", dice_size=6, dice_count=2, bonus=1)
TWO_HANDED_SWORD_2 = Weapon("Two Handed Sword +2", dice_size=6, dice_count=2, bonus=2)

TWO_HANDED_AXE_0 = Weapon("Two Handed Axe", dice_size=12)
TWO_HANDED_AXE_1 = Weapon("Two Handed Axe +1", dice_size=12, bonus=1)

RAPIER_1 = Weapon("Rapier +1", dice_size=8, bonus=1)

HUNTERS_MARK_DAMAGE = Weapon("Hunters Mark", dice_size=6)
