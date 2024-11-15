import enum


class ReplenishType(enum.Enum):
    TURN = enum.auto
    COMBAT = enum.auto
    SHORT_REST = enum.auto
    LONG_REST = enum.auto


class Resource:
    def __init__(self,
                 name: str,
                 replenish_type: ReplenishType,
                 max_value: int):
        self.name = name
        self.replenish_type = replenish_type
        self._max_value = max_value
        self.value = max_value

    @property
    def max_value(self):
        return self._max_value

    def __str__(self):
        return self.name


class ResourceRage(Resource):
    def __init__(self, name: str, replenish_type: ReplenishType, max_value: int, rage_damage: int):
        super().__init__(name, replenish_type, max_value)
        self.rage_damage = rage_damage


class ResourceSuperiorityDice(Resource):
    def __init__(self, name: str, replenish_type: ReplenishType, max_value: int, dice_size: int):
        super().__init__(name, replenish_type, max_value)
        self.dice_size = dice_size


RESOURCE_PROGRESSION_FIGHTER_CHAMPION = lambda: {
    2: {Resource("ActionSurge", ReplenishType.SHORT_REST, 1)}
}

RESOURCE_PROGRESSION_FIGHTER_BATTLE_MASTER = lambda: {
    2: {Resource("ActionSurge", ReplenishType.SHORT_REST, 1)},
    3: {ResourceSuperiorityDice("SuperiorityDice", ReplenishType.SHORT_REST, 4, 8)},
    7: {ResourceSuperiorityDice("SuperiorityDice", ReplenishType.SHORT_REST, 5, 8)},
    10: {ResourceSuperiorityDice("SuperiorityDice", ReplenishType.SHORT_REST, 5, 10)}
}

RESOURCE_PROGRESSION_BARBARIAN = lambda: {
    1: {ResourceRage("Rage", ReplenishType.LONG_REST, 2, 2)},
    3: {ResourceRage("Rage", ReplenishType.LONG_REST, 3, 2)},
    6: {ResourceRage("Rage", ReplenishType.LONG_REST, 4, 2)},
    9: {ResourceRage("Rage", ReplenishType.LONG_REST, 4, 3)},
    12: {ResourceRage("Rage", ReplenishType.LONG_REST, 5, 3)},
}
