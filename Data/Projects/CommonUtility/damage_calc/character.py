import math
import typing as t

from Data.Projects.CommonUtility.damage_calc.weapon import HEAVY_CROSSBOW_2
from weapon import HAND_CROSSBOW_1
from constants import (PROFICIENCY_BONUS_ON_LEVEL,
                       DEFAULT_TARGET_AC,
                       MAIN_ABILITY_ON_LEVEL_DEFAULT,
                       BASE_ABILITY_SIZE,
                       ATTACK_ROLL_DICE_SIZE)
from dc_logger import dc_logger
from dice import roll_dice

from weapon import (Weapon,
                    HEAVY_CROSSBOW_1)


class Character:
    SPEC_NAME_LEN = 70

    def __init__(self,
                 name: str,
                 weapon_main: Weapon,
                 weapon_offhand: Weapon = None,
                 fighting_style_archery=False,
                 fighting_style_dual_weapon=False,
                 has_feat_vanilla_sharpshooter=False,
                 loggingEnabled=False):
        self.name = name
        self.level = 1
        self.weapon_main = weapon_main
        self.weapon_offhand = weapon_offhand
        self.base_proficiency_bonus = PROFICIENCY_BONUS_ON_LEVEL[self.level]
        self.ability_proficiency_bonus = int(
            math.floor((MAIN_ABILITY_ON_LEVEL_DEFAULT[self.level] - BASE_ABILITY_SIZE) / 2))
        self.has_fighting_style_archery = fighting_style_archery
        self.has_fighting_style_dual_weapon = fighting_style_dual_weapon
        self.has_feat_vanilla_sharpshooter = has_feat_vanilla_sharpshooter
        self.spec: str = (f'{self.name} lvl {self.level} with {self.weapon_main.name}'
                          f'{" and " if self.weapon_offhand is not None else ""}'
                          f'{self.weapon_offhand.name if self.weapon_offhand is not None else ""}')
        self._debug = dc_logger.debug if loggingEnabled else lambda _: None

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

        style_bonus = 2 if self.has_fighting_style_archery else 0
        self._debug(f'Fighting Style bonus: {style_bonus}')
        attack_roll += style_bonus

        attack_roll += self.ability_proficiency_bonus
        self._debug(f'Ability proficiency bonus: {self.ability_proficiency_bonus}')

        attack_roll += weapon.bonus
        self._debug(f'Weapon bonus: {weapon.bonus}')

        if self.has_feat_vanilla_sharpshooter:
            attack_roll -= 5
            self._debug(f'Sharpshooter (vanilla): -5')

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
            return res

        if attack_roll < target_ac:
            self._debug(f"{self.name} -> 0 damage, rolled {attack_roll} against {target_ac}")
            return 0

        res = weapon.damage_roll()
        res += self.ability_proficiency_bonus if apply_proficiency_bonus else 0

        if self.has_feat_vanilla_sharpshooter:
            res += 10
            self._debug('Sharpshooter (vanilla): +10 damage')

        self._debug(f"{self.name} -> {res} damage, rolled {attack_roll} against {target_ac}")
        return res

    def main_hand_attack(self, target_ac=DEFAULT_TARGET_AC):
        self._debug(f'\tmain hand attack:')
        return self.do_attack(self.weapon_main, target_ac)

    def offhand_attack(self, target_ac=DEFAULT_TARGET_AC):
        self._debug(f'\toffhand attack:')
        return self.do_attack(self.weapon_offhand, target_ac, self.has_fighting_style_dual_weapon)

    def play_round(self, target_ac: int):
        self._debug(f'\n>>> {self.name} combat round:')
        dpr = self.main_hand_attack(target_ac)
        dpr += self.offhand_attack(target_ac) if self.weapon_offhand is not None else 0
        dpr += self.main_hand_attack(target_ac) if self.level >= 5 else 0
        return dpr


ARCHERY_SS_VANILLA = {
    1: Character("Ranger_Archery_SS_Vanilla", HEAVY_CROSSBOW_1, fighting_style_archery=True),
    4: Character("Ranger_Archery_SS_Vanilla", HEAVY_CROSSBOW_1, fighting_style_archery=True,
                 has_feat_vanilla_sharpshooter=True)
}

ARCHERY_NO_FEATS = {
    1: Character("Ranger_Archery_NoFeats", HEAVY_CROSSBOW_1, fighting_style_archery=True)
}

TWO_WEAPONS_CROSSBOWS_NO_FEATS = {
    1: Character("Ranger_TwoCrossbows_NoFeats", HAND_CROSSBOW_1, HAND_CROSSBOW_1,
                 fighting_style_dual_weapon=True)
}

TWO_WEAPONS_CROSSBOWS_SS_VANILLA = {
    1: Character("Ranger_TwoCrossbows_SS_Vanilla", HAND_CROSSBOW_1, HAND_CROSSBOW_1,
                 fighting_style_dual_weapon=True),
    4: Character("Ranger_TwoCrossbows_SS_Vanilla", HAND_CROSSBOW_1, HAND_CROSSBOW_1,
                 fighting_style_dual_weapon=True, has_feat_vanilla_sharpshooter=True)
}

ALL_PROGRESSIONS = [
    ARCHERY_SS_VANILLA,
    ARCHERY_NO_FEATS,
    TWO_WEAPONS_CROSSBOWS_NO_FEATS,
    TWO_WEAPONS_CROSSBOWS_SS_VANILLA
]

if __name__ == "__main__":
    ranger = Character("Ranger", HEAVY_CROSSBOW_2, fighting_style_archery=True)
    ranger_ss = Character("Ranger_SS", HEAVY_CROSSBOW_2, fighting_style_archery=True,
                          has_feat_vanilla_sharpshooter=True)

    ranger_ss.do_attack(ranger_ss.weapon_main, 13)
    ranger.do_attack(ranger.weapon_main, 13)
    ranger_ss.do_attack(ranger_ss.weapon_main, 13)
    ranger.do_attack(ranger.weapon_main, 13)
    ranger_ss.do_attack(ranger_ss.weapon_main, 13)
    ranger.do_attack(ranger.weapon_main, 13)
    ranger_ss.do_attack(ranger_ss.weapon_main, 13)
    ranger.do_attack(ranger.weapon_main, 13)
    ranger_ss.do_attack(ranger_ss.weapon_main, 13)
    ranger.do_attack(ranger.weapon_main, 13)
