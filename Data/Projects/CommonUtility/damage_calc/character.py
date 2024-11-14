import math
import typing as t

from attr import dataclass

from Data.Projects.CommonUtility.damage_calc.weapon import TWO_HANDED_SWORD_0
from weapon import (Weapon,
                    HAND_CROSSBOW_1,
                    HEAVY_CROSSBOW_1,
                    HEAVY_CROSSBOW_2,
                    TWO_HANDED_SWORD_1
                    )

from constants import (PROFICIENCY_BONUS_ON_LEVEL,
                       DEFAULT_TARGET_AC,
                       MAIN_ABILITY_ON_LEVEL_DEFAULT,
                       BASE_ABILITY_SIZE,
                       ATTACK_ROLL_DICE_SIZE)
from dc_logger import dc_logger
from dice import roll_dice


@dataclass
class Passives:
    passive_extra_attack = False
    passive_second_extra_attack = False
    passive_extra_offhand_attack = False

    fighting_style_archery = False
    fighting_style_two_weapon_fighting = False
    fighting_style_great_weapon_fighting = False

    feat_sharpshooter_vanilla = False
    feat_great_weapon_master_vanilla = False


class Character:
    SPEC_NAME_LEN = 70

    def __init__(self,
                 name: str,
                 weapon_main: Weapon,
                 weapon_offhand: Weapon = None,
                 logging_enabled=True):
        self.name = name
        self.level = 1
        self.weapon_main = weapon_main
        self.weapon_offhand = weapon_offhand
        self.passives = Passives()
        self._debug = dc_logger.debug if logging_enabled else lambda _: None

        self._gwm_proc = False

    @property
    def base_proficiency_bonus(self):
        return PROFICIENCY_BONUS_ON_LEVEL[self.level]

    @property
    def ability_proficiency_bonus(self):
        return int(math.floor((MAIN_ABILITY_ON_LEVEL_DEFAULT[self.level] - BASE_ABILITY_SIZE) / 2))

    def attack_roll(self, weapon: Weapon) -> t.Union[int, t.Literal["CRITICAL_MISS", "CRITICAL_HIT"]]:
        """Get attack roll with all possible bonuses and penalties"""
        attack_roll = roll_dice(ATTACK_ROLL_DICE_SIZE)
        self._debug(f'Attack dice roll: {attack_roll}')

        if attack_roll == 1:
            self._debug(f"Critical miss!")
            return "CRITICAL_MISS"
        if attack_roll == ATTACK_ROLL_DICE_SIZE:
            self._debug(f'Critical hit!')
            return "CRITICAL_HIT"

        # no crits this time, add bonuses to roll
        attack_roll += self.base_proficiency_bonus
        self._debug(f'Proficiency bonus: {self.base_proficiency_bonus}')

        style_bonus = 2 if self.passives.fighting_style_archery else 0
        self._debug(f'Fighting Style bonus: {style_bonus}')
        attack_roll += style_bonus

        attack_roll += self.ability_proficiency_bonus
        self._debug(f'Ability proficiency bonus: {self.ability_proficiency_bonus}')

        attack_roll += weapon.bonus
        self._debug(f'Weapon bonus: {weapon.bonus}')

        if self.passives.feat_sharpshooter_vanilla or self.passives.feat_great_weapon_master_vanilla:
            attack_roll -= 5
            self._debug(f'Sharpshooter/GWM (vanilla): -5')

        self._debug(f'Roll result: >> {attack_roll} <<')
        return attack_roll

    def do_attack(self, weapon: Weapon, target_ac, apply_proficiency_bonus=True) -> int:
        attack_roll = self.attack_roll(weapon)

        if attack_roll == "CRITICAL_MISS":
            self._debug(f"{self.name} -> 0 damage, Critical miss!")
            return 0

        if attack_roll == "CRITICAL_HIT":
            res = weapon.damage_roll(critical=True)
            res += self.ability_proficiency_bonus if apply_proficiency_bonus else 0
            self._debug(f"{self.name} -> {res} damage, Critical hit!")
            if weapon is self.weapon_main and self.passives.feat_great_weapon_master_vanilla:
                self._gwm_proc = True
            return res

        if attack_roll < target_ac:
            self._debug(f"{self.name} -> 0 damage, rolled {attack_roll} against {target_ac}")
            return 0

        res = weapon.damage_roll(great_weapon_fighting=self.passives.fighting_style_great_weapon_fighting)
        res += self.ability_proficiency_bonus if apply_proficiency_bonus else 0

        if self.passives.feat_sharpshooter_vanilla or self.passives.feat_great_weapon_master_vanilla:
            res += 10
            self._debug('Sharpshooter/GWM (vanilla): +10 damage')

        self._debug(f"{self.name} -> {res} damage, rolled {attack_roll} against {target_ac}")
        return res

    def main_hand_attack(self, target_ac=DEFAULT_TARGET_AC):
        self._debug(f'\tmain hand attack:')
        return self.do_attack(self.weapon_main, target_ac)

    def offhand_attack(self, target_ac=DEFAULT_TARGET_AC):
        self._debug(f'\toffhand attack:')
        return self.do_attack(self.weapon_offhand, target_ac, self.passives.fighting_style_two_weapon_fighting)

    def play_round(self, target_ac: int):
        self._debug(f'\n>>> {self.name} combat round:')
        self._gwm_proc = False
        dpr = self.main_hand_attack(target_ac)
        dpr += self.offhand_attack(target_ac) if self.weapon_offhand is not None else 0
        dpr += self.offhand_attack(
            target_ac) if self.weapon_offhand is not None and self.passives.passive_extra_offhand_attack else 0
        dpr += self.main_hand_attack(target_ac) if self.passives.passive_extra_attack else 0
        dpr += self.main_hand_attack(target_ac) if self.passives.passive_second_extra_attack else 0
        dpr += self.main_hand_attack(target_ac) if self._gwm_proc else 0
        return dpr


class ProgressionBase:
    def __init__(self, character_1_level: Character):
        self._character_map = {level: character_1_level for level in range(1, 13)}

    def get_character(self, level: int):
        assert 1 <= level <= 12
        return self._character_map[level]


PROGRESSION_BASIC = ProgressionBase(
    Character("Basic", TWO_HANDED_SWORD_0)
)

if __name__ == "__main__":
    pass
