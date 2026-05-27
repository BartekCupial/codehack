from types import SimpleNamespace

import pytest

from codehack.bot.character.properties import Alignment, Race
from codehack.bot.pvp.monster import MonsterClassTypes
from codehack.bot.strategies.fight_monster import fight_melee


class FakePathfinder:
    def __init__(self, bot):
        self.bot = bot
        self.glanced = False

    def reachable(self, start, end, adjacent=True):
        return end

    def distances(self, start):
        return {self.bot.entities[0].position: 1}

    def glance(self, position):
        self.glanced = True
        self.bot.message = "peaceful"


class FakePvp:
    def __init__(self):
        self.attacked = []

    def attack_melee(self, entity):
        self.attacked.append(entity)


def make_bot(race, monster_name, monster_class):
    entity = SimpleNamespace(
        name=monster_name,
        position=(0, 1),
        permonst=SimpleNamespace(mlet=chr(monster_class.value)),
    )
    bot = SimpleNamespace(
        character=SimpleNamespace(alignment=Alignment.UNALIGNED, race=race),
        entities=[entity],
        entity=SimpleNamespace(position=(0, 0)),
        message="",
        movements=None,
        pvp=FakePvp(),
    )
    bot.pathfinder = FakePathfinder(bot)
    return bot, entity


@pytest.mark.parametrize(
    ("race", "monster_name", "monster_class", "expected_glance"),
    [
        (Race.DWARF, "dwarf", MonsterClassTypes.S_HUMANOID, True),
        (Race.DWARF, "hobbit", MonsterClassTypes.S_HUMANOID, False),
        (Race.GNOME, "gnome", MonsterClassTypes.S_GNOME, True),
        (Race.GNOME, "dwarf", MonsterClassTypes.S_HUMANOID, True),
        (Race.ELF, "Elvenking", MonsterClassTypes.S_HUMAN, True),
        (Race.ELF, "human", MonsterClassTypes.S_HUMAN, False),
    ],
)
def test_fight_melee_race_specific_peaceful_checks(race, monster_name, monster_class, expected_glance):
    bot, entity = make_bot(race, monster_name, monster_class)

    assert fight_melee.__wrapped__(bot)
    assert bot.pathfinder.glanced is expected_glance
    assert bot.pvp.attacked == [entity]
