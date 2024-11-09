import math

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
            dc_logger.info(f"{self.name} -> 0 damage, Critical miss!")
            return 0

        if attack_roll == ATTACK_ROLL_DICE_SIZE:
            res = weapon.damage_roll(critical=True)
            res += self.ability_proficiency_bonus if apply_proficiency_bonus else 0
            dc_logger.info(f"{self.name} -> {res} damage, Critical hit!")
            return res

        style_bonus = 2 if self.has_fighting_style_archery else 0
        attack_roll = attack_roll + self.base_proficiency_bonus + self.ability_proficiency_bonus + weapon.bonus + style_bonus
        if attack_roll < target_ac:
            dc_logger.info(f"{self.name} -> 0 damage, rolled {attack_roll} against {target_ac}")
            return 0

        res = weapon.damage_roll()
        res += self.ability_proficiency_bonus if apply_proficiency_bonus else 0
        dc_logger.info(f"{self.name} -> {res} damage, rolled {attack_roll} against {target_ac}")
        return res

    def main_hand_attack(self, target_ac=DEFAULT_TARGET_AC):
        return self.do_attack(self.weapon_main, target_ac)

    def offhand_attack(self, target_ac=DEFAULT_TARGET_AC):
        return self.do_attack(self.weapon_offhand, target_ac, self.has_fighting_style_dual_weapon)

    def simulate(self, rounds=5, target_ac=DEFAULT_TARGET_AC, iterations=1000):
        results = []
        for _ in range(iterations):
            results_per_round = []
            for _ in range(rounds):
                dpr = self.main_hand_attack(target_ac)
                dpr += self.offhand_attack(target_ac) if self.weapon_offhand is not None else 0
                dpr += self.main_hand_attack(target_ac) if self.level >= 5 else 0
                results_per_round.append(dpr)
            results.append(sum(results_per_round) / rounds)
        avg_damage = sum(results) / iterations
        print(f'{self.name} lvl {self.level} with {self.weapon_main.name} '
              f'{"and " if self.weapon_offhand is not None else ""}'
              f'{self.weapon_offhand.name if self.weapon_offhand is not None else ""}, avg DPR: {avg_damage:.1f}')


RANGER_LEVEL_5_ARCHERY = Character("Ranger archery", 5, HEAVY_CROSSBOW_1, fighting_style_archery=True)


if __name__ == "__main__":
    avg_dpr = RANGER_LEVEL_5_ARCHERY.simulate()
