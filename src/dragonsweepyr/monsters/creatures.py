"""BoardTile child classes for creatures"""
from dragonsweepyr.monsters.tiles import BoardTile, TileID
from dragonsweepyr.utils import is_center, is_corner, is_edge, res_to_frame


class Bat(BoardTile):

    """Bat monster."""

    def __init__(self, monster_level: int = 2) -> None:
        """"""
        super().__init__()
        self.id = TileID.Bat
        self.strip_frame = res_to_frame(134, 231)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Bats have no locational satisfaction effect."""
        return super().satisfaction()


class BigSlime(BoardTile):

    """Big Slime monster."""

    def __init__(self, monster_level: int = 8) -> None:
        """"""
        super().__init__()
        self.id = TileID.BigSlime
        self.strip_frame = res_to_frame(120, 455)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Big Slimes have no locational satisfaction effect."""
        return super().satisfaction()


class DarkKnight(BoardTile):

    """Dark Knight monster."""

    def __init__(self, monster_level: int = 5) -> None:
        """"""
        super().__init__()
        self.id = TileID.DarkKnight
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level
        if monster_level == 5:
            self.strip_frame = res_to_frame(200, 168)
        else:  # monster_level == 7
            self.strip_frame = res_to_frame(200, 100)

    def satisfaction(self) -> int:
        """Dark Knights have no locational satisfaction effect."""
        return super().satisfaction()


class Death(BoardTile):

    """Death monster."""

    def __init__(self, monster_level: int = 9) -> None:
        """"""
        super().__init__()
        self.id = TileID.Death
        self.strip_frame = res_to_frame(130, 340)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Deaths have no locational satisfaction effect."""
        return super().satisfaction()


class Dragon(BoardTile):

    """Dragon monster."""

    def __init__(self, monster_level: int = 13) -> None:
        """"""
        super().__init__()
        self.id = TileID.Dragon
        self.strip_frame = res_to_frame(200, 311)
        self.deadStripFrame = res_to_frame(230, 310)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Dragons should be in a central region of the board."""
        if is_center(self.tx, self.ty):
            return 10000
        return 0


class DragonEgg(BoardTile):

    """Dragon egg monster."""

    def __init__(self, monster_level: int = 0) -> None:
        """"""
        super().__init__()
        self.id = TileID.DragonEgg
        self.strip_frame = res_to_frame(0, 250)
        self.deadStripFrame = self.strip_frame + 1
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = 3

    def satisfaction(self) -> int:
        """Dragon egg has no locational satisfaction effect."""
        return super().satisfaction()


class Eye(BoardTile):

    """Eye monster."""

    def __init__(self, monster_level: int = 5) -> None:
        """"""
        super().__init__()
        self.id = TileID.Eye
        self.strip_frame = res_to_frame(135, 167)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Eyes have no locational satisfaction effect."""
        return super().satisfaction()


class Fidel(BoardTile):

    """Fidel monster."""

    def __init__(self, monster_level: int = 0) -> None:
        """"""
        super().__init__()
        self.id = TileID.Fidel
        self.strip_frame = res_to_frame(0, 408)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Fidel prefers corners."""
        if is_corner(self.tx, self.ty):
            return 9000
        return 0


class Gargoyle(BoardTile):

    """Gargoyle monster."""

    def __init__(self, monster_level: int = 4) -> None:
        """"""
        super().__init__()
        self.id = TileID.Gargoyle
        self.strip_frame = res_to_frame(26, 210)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Gargoyles have no locational satisfaction effect."""
        return super().satisfaction()

    def has_twin(self, twin: BoardTile) -> bool:
        """
        Check if the gargoyle is in its correct location.

        Part of the happiness mechanic for dungeon generation. If a gargoyle has another gargoyle within 1 distance unit, it has a 'twin'.

        function isGargoyleInRightPlace(a)
        {
            let foundTwin = false;
            let neighborCount = 0;
            for(let b of state.actors)
            {
                if(a === b) continue;
                let dist = distance(a.tx, a.ty, b.tx, b.ty);
                if(dist <= 1 && b.id == ActorId.Gargoyle)
                {
                    neighborCount += 1;
                    if(b.name == a.name)
                    {
                        foundTwin = true;
                    }
                }
            }
            return foundTwin;
        }

        Returns:
            bool: True if has a twin gargoyle nearby, False otherwise.
        """
        raise NotImplementedError("Gargoyle.has_twin() is not implemented yet.")


class Gazer(BoardTile):

    """Gazer monster."""

    def __init__(self, monster_level: int = 5) -> None:
        """"""
        super().__init__()
        self.id = TileID.Gazer
        self.strip_frame = res_to_frame(135, 180)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Gazers have no locational satisfaction effect."""
        return super().satisfaction()


class Giant(BoardTile):

    """Giant monster."""

    def __init__(self, monster_level: int = 9) -> None:
        """"""
        super().__init__()
        self.id = TileID.Giant
        self.strip_frame = res_to_frame(0, 450)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Giants have no locational satisfaction effect."""
        return super().satisfaction()


class Gnome(BoardTile):

    """Gnome monster."""

    def __init__(self, monster_level: int = 0) -> None:
        """"""
        super().__init__()
        self.id = TileID.Gnome
        self.strip_frame = res_to_frame(40, 408)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = 9

    def satisfaction(self) -> int:
        """Gnomes have no locational satisfaction effect."""
        return super().satisfaction()


class Guard(BoardTile):

    """Guard monster."""

    def __init__(self, monster_level: int = 7) -> None:
        """"""
        super().__init__()
        self.id = TileID.Guard
        self.strip_frame = res_to_frame(200, 200)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Guards should be in respective quadrants based on their name."""
        match self.name:
            case "guard1":
                if self.tx < 6 and self.ty < 4:
                    return 2500
            case "guard2":
                if self.tx > 6 and self.ty < 4:
                    return 2500
            case "guard3":
                if self.tx > 6 and self.ty > 4:
                    return 2500
            case "guard4":
                if self.tx < 6 and self.ty > 4:
                    return 2500
            case _:
                raise ValueError(f"Unknown guard name: {self.name}")
        return 0


class Mimic(BoardTile):

    """Mimic monster."""

    def __init__(self, monster_level: int = 11) -> None:
        """"""
        super().__init__()
        self.id = TileID.Mimic
        self.strip_frame = res_to_frame(70, 360)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level
        self.mimicMimicking = True

    def satisfaction(self) -> int:
        """Mimics have no locational satisfaction effect."""
        return super().satisfaction()


class Mine(BoardTile):

    """Mine monster."""

    def __init__(self, monster_level: int = 100) -> None:
        """"""
        super().__init__()
        self.id = TileID.Mine
        self.strip_frame = res_to_frame(150, 455)
        self.deadStripFrame = res_to_frame(170, 455)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = 3

    def satisfaction(self) -> int:
        """Mines have no locational satisfaction effect."""
        return super().satisfaction()


class MineKing(BoardTile):

    """Mine King monster."""

    def __init__(self, monster_level: int = 10) -> None:
        """"""
        super().__init__()
        self.id = TileID.MineKing
        self.strip_frame = res_to_frame(250, 135)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """The Mine King must be in a corner."""
        if is_corner(self.tx, self.ty):
            return 10000
        return 0


class Minotaur(BoardTile):

    """Minotaur monster."""

    def __init__(self, monster_level: int = 6) -> None:
        """"""
        super().__init__()
        self.id = TileID.Minotaur
        self.strip_frame = res_to_frame(200, 326)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Minotaurs have no locational satisfaction effect."""
        return super().satisfaction()


class Rat(BoardTile):

    """Rat monster."""

    def __init__(self, monster_level: int = 1) -> None:
        """"""
        super().__init__()
        self.id = TileID.Rat
        self.strip_frame = res_to_frame(90, 265)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Rats have no locational satisfaction effect."""
        return super().satisfaction()


class RatKing(BoardTile):

    """Rat King monster."""

    def __init__(self, monster_level: int = 5) -> None:
        """"""
        super().__init__()
        self.id = TileID.RatKing
        self.strip_frame = res_to_frame(70, 265)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Rat Kings have no locational satisfaction effect."""
        return super().satisfaction()


class Skeleton(BoardTile):

    """Skeleton monster."""

    def __init__(self, monster_level: int = 3) -> None:
        """"""
        super().__init__()
        self.id = TileID.Skeleton
        self.strip_frame = res_to_frame(70, 134)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Skeletons have no locational satisfaction effect."""
        return super().satisfaction()


class Slime(BoardTile):

    """Slime monster."""

    def __init__(self, monster_level: int = 5) -> None:
        """"""
        super().__init__()
        self.id = TileID.Slime
        self.strip_frame = res_to_frame(86, 473)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Slimes have no locational satisfaction effect."""
        return super().satisfaction()


class Snake(BoardTile):

    """Snake monster."""

    def __init__(self, monster_level: int = 7) -> None:
        """"""
        super().__init__()
        self.id = TileID.Snake
        self.strip_frame = res_to_frame(250, 250)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Snakes have no locational satisfaction effect."""
        return super().satisfaction()


class Wizard(BoardTile):

    """Wizard monster."""

    def __init__(self, monster_level: int = 1) -> None:
        """"""
        super().__init__()
        self.id = TileID.Wizard
        self.strip_frame = res_to_frame(72, 76)
        self.isMonster = True
        self.monster_level = monster_level
        self.xp = monster_level

    def satisfaction(self) -> int:
        """Wizards should be along and edge but not in a corner."""
        if is_edge(self.tx, self.ty) and not is_corner(self.tx, self.ty):
            return 10000
        return 0
