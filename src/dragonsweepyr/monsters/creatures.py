"""BoardTile child classes for creatures"""
from dragonsweepyr.monsters.tiles import BoardTile, TileID
from dragonsweepyr.utils import res_to_frame


class Bat(BoardTile):

    """Bat monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Bat
        self.stripFrame = res_to_frame(134, 231)
        self.isMonster = True
        self.monsterLevel = 2
        self.xp = 2


class BigSlime(BoardTile):

    """Big Slime monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.BigSlime
        self.stripFrame = res_to_frame(120, 455)
        self.isMonster = True
        self.monsterLevel = 8
        self.xp = 8


class DarkKnight(BoardTile):

    """Dark Knight monster."""

    def __init__(self, level: int = 5) -> None:
        """"""
        super().__init__()
        self.id = TileID.DarkKnight
        self.isMonster = True
        self.monsterLevel = level
        self.xp = level
        if level == 5:
            self.stripFrame = res_to_frame(200, 168)
        else:  # level == 7
            self.stripFrame = res_to_frame(200, 100)


class Death(BoardTile):

    """Death monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Death
        self.stripFrame = res_to_frame(130, 340)
        self.isMonster = True
        self.monsterLevel = 9
        self.xp = 9


class Dragon(BoardTile):

    """Dragon monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Dragon
        self.stripFrame = res_to_frame(200, 311)
        self.deadStripFrame = res_to_frame(230, 310)
        self.isMonster = True
        self.monsterLevel = 13
        self.xp = 13


class DragonEgg(BoardTile):

    """Dragon egg monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.DragonEgg
        self.stripFrame = res_to_frame(0, 250)
        self.deadStripFrame = self.stripFrame + 1
        self.isMonster = True
        self.monsterLevel = 0
        self.xp = 3


class Eye(BoardTile):

    """Eye monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Eye
        self.stripFrame = res_to_frame(135, 167)
        self.isMonster = True
        self.monsterLevel = 5
        self.xp = 5


class Fidel(BoardTile):

    """Fidel monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Fidel
        self.stripFrame = res_to_frame(0, 408)
        self.isMonster = True
        self.monsterLevel = 0
        self.xp = 0


class Gargoyle(BoardTile):

    """Gargoyle monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Gargoyle
        self.stripFrame = res_to_frame(26, 210)
        self.isMonster = True
        self.monsterLevel = 4
        self.xp = 4

    def has_twin(self, ) -> bool:
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

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Gazer
        self.stripFrame = res_to_frame(135, 180)
        self.isMonster = True
        self.monsterLevel = 5
        self.xp = 5


class Giant(BoardTile):

    """Giant monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Giant
        self.stripFrame = res_to_frame(0, 450)
        self.isMonster = True
        self.monsterLevel = 9
        self.xp = 9


class Gnome(BoardTile):

    """Gnome monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Gnome
        self.stripFrame = res_to_frame(40, 408)
        self.isMonster = True
        self.monsterLevel = 0
        self.xp = 9


class Guard(BoardTile):

    """Guard monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Guard
        self.stripFrame = res_to_frame(200, 200)
        self.isMonster = True
        self.monsterLevel = 7
        self.xp = 7


class Mimic(BoardTile):

    """Mimic monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Mimic
        self.stripFrame = res_to_frame(70, 360)
        self.isMonster = True
        self.monsterLevel = 11
        self.xp = 11
        self.mimicMimicking = True


class Mine(BoardTile):

    """Mine monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Mine
        self.stripFrame = res_to_frame(150, 455)
        self.deadStripFrame = res_to_frame(170, 455)
        self.isMonster = True
        self.monsterLevel = 100
        self.xp = 3


class MineKing(BoardTile):

    """Mine King monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.MineKing
        self.stripFrame = res_to_frame(250, 135)
        self.isMonster = True
        self.monsterLevel = 10
        self.xp = 10


class Minotaur(BoardTile):

    """Minotaur monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Minotaur
        self.stripFrame = res_to_frame(200, 326)
        self.isMonster = True
        self.monsterLevel = 6
        self.xp = 6


class Rat(BoardTile):

    """Rat monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Rat
        self.stripFrame = res_to_frame(90, 265)
        self.isMonster = True
        self.monsterLevel = 1
        self.xp = 1


class RatKing(BoardTile):

    """Rat King monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.RatKing
        self.stripFrame = res_to_frame(70, 265)
        self.isMonster = True
        self.monsterLevel = 5
        self.xp = 5


class Skeleton(BoardTile):

    """Skeleton monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Skeleton
        self.stripFrame = res_to_frame(70, 134)
        self.isMonster = True
        self.monsterLevel = 3
        self.xp = 3


class Slime(BoardTile):

    """Slime monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Slime
        self.stripFrame = res_to_frame(86, 473)
        self.isMonster = True
        self.monsterLevel = 5
        self.xp = 5


class Snake(BoardTile):

    """Snake monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Snake
        self.stripFrame = res_to_frame(250, 250)
        self.isMonster = True
        self.monsterLevel = 7
        self.xp = 7


class Wizard(BoardTile):

    """Wizard monster."""

    def __init__(self) -> None:
        """"""
        super().__init__()
        self.id = TileID.Wizard
        self.stripFrame = res_to_frame(72, 76)
        self.isMonster = True
        self.monsterLevel = 1
        self.xp = 1
