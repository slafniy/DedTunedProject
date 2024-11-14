import enum
import logging
import math
import typing as t

import weapon as wpn
from dc_logger import get_logger

from constants import (PROFICIENCY_BONUS_ON_LEVEL,
                       DEFAULT_TARGET_AC,
                       MAIN_ABILITY_PROGRESSION_DT,
                       BASE_ABILITY_SIZE,
                       ATTACK_ROLL_DICE_SIZE)
from dice import roll_dice


class Passive(enum.Enum):
    PASSIVE_EXTRA_ATTACK = enum.auto()
    PASSIVE_SECOND_EXTRA_ATTACK = enum.auto()

    FIGHTING_STYLE_ARCHERY = enum.auto()
    FIGHTING_STYLE_TWO_WEAPON_FIGHTING = enum.auto()
    FIGHTING_STYLE_GREAT_WEAPON_FIGHTING = enum.auto()

    FEAT_EXTRA_OFFHAND_ATTACK = enum.auto()
    FEAT_SHARPSHOOTER_VANILLA = enum.auto()
    FEAT_GREAT_WEAPON_MASTER_VANILLA = enum.auto()
    # FEAT_GREAT_WEAPON_MASTER_3x6 = enum.auto()


logger = get_logger("Character")


class Character:
    MAX_LEVEL = 12

    def __init__(self,
                 name: str,
                 weapon_main: wpn.Weapon,
                 weapon_offhand: wpn.Weapon = None,
                 passives_progression: t.Dict[int, t.Set[Passive]] = {},
                 main_ability_progression: t.Dict[int, int] = MAIN_ABILITY_PROGRESSION_DT):
        self.name = name
        self._level = 1
        self._weapon_main = weapon_main
        self._weapon_offhand = weapon_offhand
        self._passives_progression: t.Dict[int, t.Set[Passive]] = passives_progression
        self._main_ability_progression: t.Dict[int, int] = main_ability_progression
        self._base_proficiency_progression: t.Dict[int, int] = PROFICIENCY_BONUS_ON_LEVEL

        self._gwm_proc = False
        self._passives: t.Set[Passive] = set()
        self._apply_passives()

    def _apply_passives(self):
        self._passives = set()
        for level in range(1, self._level + 1):
            self._passives.update(
                self._passives_progression.get(level, set())
            )

    def drop_to_level_1(self):
        self._level = 1
        self._apply_passives()

    def level_up(self, levels=1) -> bool:
        """Add levels, returns False if is already on max level"""
        if self._level >= self.MAX_LEVEL:
            return False

        for _ in range(levels):
            if self._level < self.MAX_LEVEL:
                self._level += 1
                self._apply_passives()
        return True

    @property
    def level(self):
        return self._level

    @property
    def base_proficiency_bonus(self):
        return self._base_proficiency_progression[self._level]

    @property
    def ability_proficiency_bonus(self):
        return int(math.floor((self._main_ability_progression[self._level] - BASE_ABILITY_SIZE) / 2))

    def attack_roll(self, weapon: wpn.Weapon) -> t.Union[int, t.Literal["CRITICAL_MISS", "CRITICAL_HIT"]]:
        """Get attack roll with all possible bonuses and penalties"""
        attack_roll = roll_dice(ATTACK_ROLL_DICE_SIZE)
        logger.debug(f'Attack dice roll: {attack_roll}')

        if attack_roll == 1:
            logger.debug(f"Critical miss!")
            return "CRITICAL_MISS"
        if attack_roll == ATTACK_ROLL_DICE_SIZE:
            logger.debug(f'Critical hit!')
            return "CRITICAL_HIT"

        # no crits this time, add bonuses to roll
        attack_roll += self.base_proficiency_bonus
        logger.debug(f'Proficiency bonus: {self.base_proficiency_bonus}')

        style_bonus = 2 if Passive.FIGHTING_STYLE_ARCHERY in self._passives else 0
        logger.debug(f'Fighting Style bonus: {style_bonus}')
        attack_roll += style_bonus

        attack_roll += self.ability_proficiency_bonus
        logger.debug(f'Ability proficiency bonus: {self.ability_proficiency_bonus}')

        attack_roll += weapon.bonus
        logger.debug(f'Weapon bonus: {weapon.bonus}')

        if Passive.FEAT_SHARPSHOOTER_VANILLA in self._passives or Passive.FEAT_GREAT_WEAPON_MASTER_VANILLA in self._passives:
            attack_roll -= 5
            logger.debug(f'Sharpshooter/GWM (vanilla): -5')

        logger.debug(f'Roll result: >> {attack_roll} <<')
        return attack_roll

    def do_attack(self, weapon: wpn.Weapon, target_ac, apply_proficiency_bonus=True) -> int:
        attack_roll = self.attack_roll(weapon)

        if attack_roll == "CRITICAL_MISS":
            logger.debug(f"0 damage, Critical miss!")
            return 0

        if attack_roll != "CRITICAL_HIT" and attack_roll < target_ac:
            logger.debug(f"0 damage, rolled {attack_roll} against {target_ac}")
            return 0

        if attack_roll == "CRITICAL_HIT":
            res = weapon.damage_roll(critical=True, logger=logger)
            logger.debug(f"{res} damage, Critical hit!")
            if weapon is self._weapon_main and Passive.FEAT_GREAT_WEAPON_MASTER_VANILLA in self._passives:
                self._gwm_proc = True
        else:  # normal hit
            res = weapon.damage_roll(great_weapon_fighting=Passive.FIGHTING_STYLE_GREAT_WEAPON_FIGHTING in self._passives,
                                     logger=logger)

        res += self.ability_proficiency_bonus if apply_proficiency_bonus else 0
        if Passive.FEAT_SHARPSHOOTER_VANILLA in self._passives or Passive.FEAT_GREAT_WEAPON_MASTER_VANILLA in self._passives:
            res += 10
            logger.debug('Sharpshooter/GWM (vanilla): +10 damage')

        logger.debug(f"{res} damage, rolled {attack_roll} against {target_ac}")
        return res

    def main_hand_attack(self, target_ac=DEFAULT_TARGET_AC):
        logger.debug(f'Main hand attack:')
        return self.do_attack(self._weapon_main, target_ac)

    def offhand_attack(self, target_ac=DEFAULT_TARGET_AC):
        logger.debug(f'Offhand attack:')
        return self.do_attack(self._weapon_offhand, target_ac,
                              Passive.FIGHTING_STYLE_TWO_WEAPON_FIGHTING in self._passives)

    def play_round(self, target_ac: int):
        self._gwm_proc = False
        dpr = self.main_hand_attack(target_ac)
        dpr += self.offhand_attack(target_ac) if self._weapon_offhand is not None else 0
        dpr += self.offhand_attack(
            target_ac) if self._weapon_offhand is not None and Passive.FEAT_EXTRA_OFFHAND_ATTACK in self._passives else 0
        dpr += self.main_hand_attack(target_ac) if Passive.PASSIVE_EXTRA_ATTACK in self._passives else 0
        dpr += self.main_hand_attack(target_ac) if Passive.PASSIVE_SECOND_EXTRA_ATTACK in self._passives else 0
        dpr += self.main_hand_attack(target_ac) if self._gwm_proc else 0
        logger.info(f"DPR: {dpr}")
        return dpr


if __name__ == "__main__":
    logger.stream_handler.setLevel(logging.DEBUG)

    c1 = Character("Fighter Big Sword + GWM", weapon_main=wpn.TWO_HANDED_SWORD_1,
                   passives_progression={
                       1: {Passive.FIGHTING_STYLE_GREAT_WEAPON_FIGHTING},
                       4: {Passive.FEAT_GREAT_WEAPON_MASTER_VANILLA},
                       5: {Passive.PASSIVE_EXTRA_ATTACK}
                   })

    c1.level_up(4)
    c1.play_round(13)
