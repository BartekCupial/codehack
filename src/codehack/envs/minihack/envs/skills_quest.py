from codehack.envs.minihack.resources import des_file
from minihack import MiniHackSkill
from minihack.envs import register


class MiniHackMonsterlessQuestEasy(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file=des_file("monsterless_quest_easy.des"), **kwargs)


class MiniHackMonsterlessQuestMedium(MiniHackSkill):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file=des_file("monsterless_quest_medium.des"), **kwargs)


register(
    id="CustomMiniHack-MonsterlessQuest-Easy-v0",
    entry_point="codehack.envs.minihack.envs.skills_quest:MiniHackMonsterlessQuestEasy",
)

register(
    id="CustomMiniHack-MonsterlessQuest-Medium-v0",
    entry_point="codehack.envs.minihack.envs.skills_quest:MiniHackMonsterlessQuestMedium",
)
