from codehack.bot import Bot
from codehack.bot.strategy import strategy


@strategy
def wield_melee_weapon(bot: "Bot"):
    return bot.pvp.wield_best_melee_weapon()


@strategy
def wield_ranged_set(bot: "Bot"):
    return bot.pvp.wield_best_ranged_set()
