import math

from Data.Projects.CommonUtility.damage_calc.weapon import HAND_CROSSBOW_1
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

    def __init__(self, name: str,
                 level: int,
                 weapon_main: Weapon,
                 weapon_offhand: Weapon = None,
                 fighting_style_archery=False,
                 fighting_style_dual_weapon=False):
        self.name = name
        self.level = level
        self.weapon_main = weapon_main
        self.weapon_offhand = weapon_offhand
        self.base_proficiency_bonus = PROFICIENCY_BONUS_ON_LEVEL[level]
        self.ability_proficiency_bonus = int(math.floor((MAIN_ABILITY_ON_LEVEL_DEFAULT[level] - BASE_ABILITY_SIZE) / 2))
        self.has_fighting_style_archery = fighting_style_archery
        self.has_fighting_style_dual_weapon = fighting_style_dual_weapon

    def do_attack(self, weapon: Weapon, target_ac, apply_proficiency_bonus=True) -> int:
        attack_roll = roll_dice(ATTACK_ROLL_DICE_SIZE)
        if attack_roll == 1:
            dc_logger.debug(f"{self.name} -> 0 damage, Critical miss!")
            return 0

        if attack_roll == ATTACK_ROLL_DICE_SIZE:
            res = weapon.damage_roll(critical=True)
            res += self.ability_proficiency_bonus if apply_proficiency_bonus else 0
            dc_logger.debug(f"{self.name} -> {res} damage, Critical hit!")
            return res

        style_bonus = 2 if self.has_fighting_style_archery else 0
        attack_roll = attack_roll + self.base_proficiency_bonus + self.ability_proficiency_bonus + weapon.bonus + style_bonus
        if attack_roll < target_ac:
            dc_logger.debug(f"{self.name} -> 0 damage, rolled {attack_roll} against {target_ac}")
            return 0

        res = weapon.damage_roll()
        res += self.ability_proficiency_bonus if apply_proficiency_bonus else 0
        dc_logger.debug(f"{self.name} -> {res} damage, rolled {attack_roll} against {target_ac}")
        return res

    def main_hand_attack(self, target_ac=DEFAULT_TARGET_AC):
        return self.do_attack(self.weapon_main, target_ac)

    def offhand_attack(self, target_ac=DEFAULT_TARGET_AC):
        return self.do_attack(self.weapon_offhand, target_ac, self.has_fighting_style_dual_weapon)

    def simulate(self, rounds=5, target_ac=DEFAULT_TARGET_AC, iterations=1000):
        results = []
        raw_rounds = []
        worst_combat_dpr = 0
        best_combat_dpr = 0
        for _ in range(iterations):
            results_per_round = []
            for _ in range(rounds):
                dpr = self.main_hand_attack(target_ac)
                dpr += self.offhand_attack(target_ac) if self.weapon_offhand is not None else 0
                dpr += self.main_hand_attack(target_ac) if self.level >= 5 else 0
                results_per_round.append(dpr)
            raw_rounds.append(results_per_round)
            combat_dpr = sum(results_per_round) / rounds
            worst_combat_dpr = min(worst_combat_dpr, combat_dpr)
            best_combat_dpr = max(best_combat_dpr, combat_dpr)
            results.append(combat_dpr)
        avg_damage = sum(results) / iterations
        spec_name = f'{self.name} lvl {self.level} with {self.weapon_main.name} {"and " if self.weapon_offhand is not None else ""} {self.weapon_offhand.name if self.weapon_offhand is not None else ""}'
        spec_name += ' ' * (self.SPEC_NAME_LEN - len(spec_name))
        print(f'{spec_name}, avg DPR: {avg_damage:.1f}, Worst combat DPR: {worst_combat_dpr:.1f}, Best combat DPR: {best_combat_dpr:.1f}')
        return raw_rounds


RANGER_LEVEL_5_ARCHERY = Character("Ranger archery", 5, HEAVY_CROSSBOW_1, fighting_style_archery=True)
RANGER_LEVEL_5_DUAL = Character("Ranger dual", 5, HAND_CROSSBOW_1, HAND_CROSSBOW_1,
                                fighting_style_dual_weapon=True)
RANGER_LEVEL_5_ARCHERY_DUAL = Character("Ranger dual", 5, HAND_CROSSBOW_1, HAND_CROSSBOW_1,
                                fighting_style_archery=True)

if __name__ == "__main__":
    AC = 20
    RANGER_LEVEL_5_ARCHERY.simulate(target_ac=AC)
    RANGER_LEVEL_5_DUAL.simulate(target_ac=AC)
    RANGER_LEVEL_5_ARCHERY_DUAL.simulate(target_ac=AC)
