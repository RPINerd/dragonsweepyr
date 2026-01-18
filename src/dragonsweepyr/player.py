"""Player character module."""

from __future__ import annotations

from typing import ClassVar

from dragonsweepyr.utils import is_level_halfheart


class Player:

    """
    Represents the player character.

    Character stats and level progression:
    Level: 1   2  3  4  5   6   7   8   9  10  11  12  13  14  15
    HP:    5      6     7       8       9      10      11      12
    """

    xp_lut: ClassVar[list[int]] = [0, 4, 5, 7, 9, 9, 10, 12, 12, 12, 15, 18, 21, 21, 25]
    hp_cap: ClassVar[int] = 19

    def __init__(self) -> None:
        self.max_hp = 4
        self.current_hp = self.max_hp
        self.xp = 0
        self.level = 1
        self.score = 0

    def gain_xp(self, amount: int) -> None:
        """Increase player's XP by the specified amount."""
        self.xp += amount
        self.score += amount

    def lose_hp(self, amount: int) -> None:
        """Decrease player's current HP by the specified amount."""
        self.current_hp -= amount

        if self.current_hp < 0:
            raise NotImplementedError("Player death not implemented yet.")

    def heal(self, amount: int = 100) -> None:
        """Heal the player, currently only full heal"""
        self.current_hp = min(self.current_hp + amount, self.max_hp)

    def level_up(self) -> None:
        """Increase player's level by 1 and adjust max HP."""
        self.xp -= self.xp_to_next_level(self.level)
        self.level += 1

        if self.max_hp < Player.hp_cap and not is_level_halfheart(self.level):
            self.max_hp += 1

        self.current_hp = self.max_hp

    @staticmethod
    def xp_to_next_level(level: int) -> int:
        """Return the number of XP required to reach the next level"""
        player_stat = min(level, len(Player.xp_lut) - 1)
        return Player.xp_lut[player_stat]
