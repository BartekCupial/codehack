from codehack.bot import Bot
from codehack.bot.exceptions import LostHP


def lost_hp(bot: "Bot"):
    current_hp = bot.blstats.hitpoints
    last_hp = bot.get_blstats(bot.last_obs).hitpoints

    if current_hp < last_hp:
        raise LostHP
