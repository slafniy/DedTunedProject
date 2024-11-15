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
from resource import Resource, ReplenishType, ResourceRage


class Passive(enum.Enum):
    PASSIVE_EXTRA_ATTACK = enum.auto()
    PASSIVE_SECOND_EXTRA_ATTACK = enum.auto()
    PASSIVE_RECKLESS_ATTACK = enum.auto()  # Constant advantage, for Barbarian
    PASSIVE_HUNTERS_MARK = enum.auto()  # For Ranger consider it as a permanent buff

    FIGHTING_STYLE_ARCHERY = enum.auto()
    FIGHTING_STYLE_TWO_WEAPON_FIGHTING = enum.auto()
    FIGHTING_STYLE_GREAT_WEAPON_FIGHTING = enum.auto()

    FEAT_EXTRA_OFFHAND_ATTACK = enum.auto()
    FEAT_SHARPSHOOTER_VANILLA = enum.auto()
    FEAT_SHARPSHOOTER_DT = enum.auto()
    FEAT_GREAT_WEAPON_MASTER_VANILLA = enum.auto()
    FEAT_GREAT_WEAPON_MASTER_DT = enum.auto()
    FEAT_SAVAGE_ATTACKER = enum.auto()


logger = get_logger("Character")


class Character:
    MAX_LEVEL = 12

    def __init__(self,
                 name: str,
                 weapon_main: wpn.Weapon,
                 weapon_offhand: wpn.Weapon = None,
                 passives_progression: t.Dict[int, t.Set[Passive]] = None,
                 resource_progression: t.Dict[int, t.Set[Resource]] = None,
                 main_ability_progression: t.Dict[int, int] = MAIN_ABILITY_PROGRESSION_DT):
        self.name = name
        self._level = 1
        self._weapon_main = weapon_main
        self._weapon_offhand = weapon_offhand
        self._passives_progression: t.Dict[int, t.Set[Passive]] = passives_progression or {}
        self._resource_progression: t.Dict[int, t.Set[Resource]] = resource_progression or {}
        self._main_ability_progression: t.Dict[int, int] = main_ability_progression
        self._base_proficiency_progression: t.Dict[int, int] = PROFICIENCY_BONUS_ON_LEVEL

        self._passives: t.Set[Passive] = set()
        self._resources: t.Dict[str, Resource] = {}
        self._apply_progressions()

        self._gwm_proc = False
        self._gwm_proc_used = False  # TODO: remade

    def short_rest(self):
        self._gwm_proc_used = False
        for r in self._resources.values():
            if r.replenish_type != ReplenishType.LONG_REST:
                r.value = r.max_value

    def long_rest(self):
        self._gwm_proc_used = False
        for r in self._resources.values():
            r.value = r.max_value

    def _apply_progressions(self):
        self._passives = set()
        self._resources = dict()
        for level in range(1, self._level + 1):
            self._passives.update(
                self._passives_progression.get(level, set())
            )
            for resource in self._resource_progression.get(level, set()):
                self._resources[resource.name] = resource

    def drop_to_level_1(self):
        self._level = 1
        self._apply_progressions()
        self.long_rest()

    def level_up(self, levels=1) -> bool:
        """Add levels, returns False if is already on max level, restore resources"""
        if self._level >= self.MAX_LEVEL:
            return False

        self._level = min(self._level + levels, self.MAX_LEVEL)

        self._apply_progressions()
        self.long_rest()
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

        if Passive.PASSIVE_RECKLESS_ATTACK in self._passives:
            attack_roll = max(attack_roll, roll_dice(ATTACK_ROLL_DICE_SIZE))

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

        attack_roll += self._rage_damage()

        # if Passive.FEAT_SHARPSHOOTER_DT in self._passives:
        #     attack_roll += 3

        if Passive.FEAT_SHARPSHOOTER_VANILLA in self._passives or Passive.FEAT_GREAT_WEAPON_MASTER_VANILLA in self._passives:
            attack_roll -= 5
            logger.debug(f'Sharpshooter/GWM (vanilla): -5')

        if Passive.FEAT_GREAT_WEAPON_MASTER_DT in self._passives:
            attack_roll -= 3
            logger.debug('GWM DT: -3')

        logger.debug(f'Roll result: >> {attack_roll} <<')
        return attack_roll

    def _damage_roll_respect_feats(self, weapon: wpn.Weapon):
        """Damage roll which respects Savage Attacker and GWF"""
        damage = roll_dice(weapon.dice_size)
        if damage in (1, 2) and Passive.FIGHTING_STYLE_GREAT_WEAPON_FIGHTING in self._passives:
            damage = roll_dice(weapon.dice_size)
        if Passive.FEAT_SAVAGE_ATTACKER in self._passives:
            damage = max(damage, roll_dice(weapon.dice_size))
        return damage

    def damage_roll(self, weapon: wpn.Weapon, critical=False) -> int:
        """Only weapon damage, basic dice + basic enchantment, also process critical hits"""
        dice_count = weapon.dice_count * 2 if critical else weapon.dice_count
        res = 0
        for _ in range(dice_count):
            damage = self._damage_roll_respect_feats(weapon)
            logger.debug(f"Damage roll: {damage} | d{weapon.dice_size}")
            res += damage
        res += weapon.bonus
        if logger:
            logger.info(
                f"Damage: {res} | {dice_count}d{weapon.dice_size} + {weapon.bonus}{' CRITICAL' if critical else ''}")
        return res

    def do_attack(self, weapon: wpn.Weapon, target_ac, apply_proficiency_bonus=True) -> int:
        attack_roll = self.attack_roll(weapon)

        if attack_roll == "CRITICAL_MISS":
            logger.debug(f"0 damage, Critical miss!")
            return 0

        if attack_roll != "CRITICAL_HIT" and attack_roll < target_ac:
            logger.debug(f"0 damage, rolled {attack_roll} against {target_ac}")
            return 0

        if attack_roll == "CRITICAL_HIT":
            res = self.damage_roll(weapon, critical=True)
            logger.debug(f"{res} damage, Critical hit!")
            if weapon is self._weapon_main and Passive.FEAT_GREAT_WEAPON_MASTER_VANILLA in self._passives:
                self._gwm_proc = True
        else:  # normal hit
            res = self.damage_roll(weapon)

        res += self.ability_proficiency_bonus if apply_proficiency_bonus else 0

        if Passive.PASSIVE_HUNTERS_MARK in self._passives:
            res += self.damage_roll(wpn.HUNTERS_MARK_DAMAGE,
                                    critical=attack_roll == "CRITICAL_HIT")  # TODO: not sure it can crit
            logger.debug("Hunter's mark bonus!")

        if Passive.FEAT_SHARPSHOOTER_DT in self._passives:
            res += self.ability_proficiency_bonus
            logger.debug('SS DT bonus')

        if Passive.FEAT_SHARPSHOOTER_VANILLA in self._passives or Passive.FEAT_GREAT_WEAPON_MASTER_VANILLA in self._passives:
            res += 10
            logger.debug('Sharpshooter/GWM (vanilla): +10 damage')

        if Passive.FEAT_GREAT_WEAPON_MASTER_DT in self._passives:
            res += 6
            logger.debug('GWM DT: +6 damage')

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
        dpr = self.main_hand_attack(target_ac)
        dpr += self.offhand_attack(target_ac) if self._weapon_offhand is not None else 0
        dpr += self.offhand_attack(
            target_ac) if self._weapon_offhand is not None and Passive.FEAT_EXTRA_OFFHAND_ATTACK in self._passives else 0
        dpr += self.main_hand_attack(target_ac) if Passive.PASSIVE_EXTRA_ATTACK in self._passives else 0
        dpr += self.main_hand_attack(target_ac) if Passive.PASSIVE_SECOND_EXTRA_ATTACK in self._passives else 0

        if self._gwm_proc and not self._gwm_proc_used:
            dpr += self.main_hand_attack(target_ac)
            self._gwm_proc_used = True
            self._gwm_proc = False

        dpr += self._process_action_surge(target_ac)

        logger.info(f"DPR: {dpr}")
        return dpr

    def _process_action_surge(self, target_ac) -> int:
        """do an additional attack(s)"""
        action_surge = self._resources.get('ActionSurge', None)
        if action_surge is None or action_surge.value == 0:
            return 0

        action_surge.value -= 1
        dpr = self.main_hand_attack(target_ac)
        dpr += self.main_hand_attack(target_ac) if Passive.PASSIVE_EXTRA_ATTACK in self._passives else 0
        dpr += self.main_hand_attack(target_ac) if Passive.PASSIVE_SECOND_EXTRA_ATTACK in self._passives else 0
        return dpr

    def _rage_damage(self):
        if "Rage" not in self._resources:
            return 0
        if isinstance(self._resources["Rage"], ResourceRage):
            return self._resources["Rage"].rage_damage  # TODO: remade


if __name__ == "__main__":
    logger.stream_handler.setLevel(logging.DEBUG)

    c1 = Character("Ranger Heavy Crossbow + SS_DT", wpn.HEAVY_CROSSBOW_1,
                   passives_progression={
                       1: {Passive.FIGHTING_STYLE_ARCHERY},
                       2: {Passive.PASSIVE_HUNTERS_MARK},
                       4: {Passive.FEAT_SHARPSHOOTER_DT},
                       5: {Passive.PASSIVE_EXTRA_ATTACK}
                   })

    c1.level_up(4)
    c1.play_round(13)
