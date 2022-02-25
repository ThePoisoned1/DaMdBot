from dataclasses import dataclass, field


@dataclass
class Skill():
    skillType: str
    name: str

    @staticmethod
    def from_csv_val(val):
        vals = val.split(': ')
        return Skill(vals[0], vals[1])


@dataclass
class Weapon():
    id: int
    weaponType: str


@dataclass
class Element():
    id: int
    elementName: str


@dataclass
class Chara():
    id: int
    charaName: str
    unitName: str
    rarity: int
    weapon: Weapon
    element: Element
    hp: int
    mp: int
    atk: int
    deff: int
    crit: int
    swordSkills: list = field(default_factory=list)
    battleSkills: list = field(default_factory=list)
    specialSkills: list = field(default_factory=list)
    upgradedStats: dict = field(default_factory=dict)
    charaPics :list=field(default_factory=list)

    def to_db(self):
        return [
            self.id,
            self.charaName,
            self.unitName,
            self.rarity,
            self.weapon,
            self.element,
            self.hp,
            self.mp,
            self.atk,
            self.deff,
            self.crit,
            ','.join(
                [f'{swordSkill.skillType}|{swordSkill.name}'for swordSkill in self.swordSkills]),
            ','.join(
                [f'{swordSkill.skillType}|{swordSkill.name}'for swordSkill in self.battleSkills]),
            ','.join(self.specialSkills),
            ','.join([f'{key}|{val}' for key, val in self.upgradedStats.items()]),
            ','.join(self.charaPics)
        ]

    @staticmethod
    def from_db(data:tuple):
        upgradedStats = {}
        if data[14]:
            for stat in data[14].split(','):
                info = stat.split('|')
                upgradedStats[info[0]]=info[1]
        return Chara(data[0],
            data[1],
            data[2],
            data[3],
            data[4],
            data[5],
            data[6],
            data[7],
            data[8],
            data[9],
            data[10],
            [Skill(skillData.split('|')[0],skillData.split('|')[1]) for  skillData in data[11].split(',')],
            [Skill(skillData.split('|')[0],skillData.split('|')[1]) for  skillData in data[12].split(',')] if data[12] else [],
            data[13].split(','),
            upgradedStats,
            data[15].split(','))

    @staticmethod
    def get_upgraded_stats_from_csv_field(data):
        stats = {}
        for val in data.split('|'):
            aux = val.split(': ')
            stats[aux[0]]=aux[1]
        return stats
        

    @staticmethod
    def from_csv_line(line: list,picUrls):
        return Chara(
            line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10],
            [Skill.from_csv_val(val) for val in line[11].split('|')],
            [Skill.from_csv_val(val) for val in line[12].split('|')] if line[12] else [],
            line[13].split('|'),
            Chara.get_upgraded_stats_from_csv_field(line[14]) if line[14] else {},
            picUrls
        )
