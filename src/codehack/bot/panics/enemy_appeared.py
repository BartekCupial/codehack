from collections import defaultdict

from codehack.bot import Bot
from codehack.bot.exceptions import EnemyAppeared
from codehack.bot.pathfinder.movements import Movements
from codehack.bot.pvp.monster import MonsterClassTypes


def enemy_appeared(bot: "Bot"):
    monster_collistion = bot.movements.monster_collision
    bot.movements.monster_collision = False

    last_entities = defaultdict(int)
    current_entities = defaultdict(int)

    # Count entities from current observation
    for entity in bot.entities:
        if bot.pathfinder.reachable(bot.entity.position, entity.position, adjacent=True):
            if not MonsterClassTypes.always_peaceful(entity.name):
                current_entities[entity.glyph] += 1

    # Count entities from previous observation
    for entity in bot.get_entities(bot.last_obs):
        if bot.pathfinder.reachable(bot.entity.position, entity.position, adjacent=True):
            if not MonsterClassTypes.always_peaceful(entity.name):
                last_entities[entity.glyph] += 1

    bot.movements.monster_collision = monster_collistion

    # Check for new enemies by comparing counts
    for glyph, count in current_entities.items():
        # If there are more entities of this type now than before
        if count > last_entities[glyph]:
            # raise Panic if new enemies appeared
            raise EnemyAppeared
