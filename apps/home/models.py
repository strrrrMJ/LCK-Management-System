from apps import db


class PlayerInfo(db.Model):
    __tablename__ = "PlayerInfo"

    name = db.Column(db.String(30), primary_key=True)
    id = db.Column(db.String(30), nullable=False)
    birthday = db.Column(db.String(50), nullable=False)
    residency = db.Column(db.String(30), nullable=False)


class PlayerData(db.Model):
    __tablename__ = "PlayerData"

    year = db.Column(db.Integer(), primary_key=True)
    season = db.Column(db.Enum("Spring", "Summer"), primary_key=True)
    id = db.Column(db.String(30), primary_key=True)
    team_name = db.Column(db.String(30), nullable=False)
    g = db.Column(db.Integer(), nullable=False)  # 比赛场数
    w = db.Column(db.Integer(), nullable=False)  # 胜场数
    l = db.Column(db.Integer(), nullable=False)  # 败场数
    wr = db.Column(db.Float(), nullable=False)  # 胜率
    k = db.Column(db.Float(), nullable=False)  # 场均击杀
    d = db.Column(db.Float(), nullable=False)  # 场均死亡
    a = db.Column(db.Float(), nullable=False)  # 场均助攻
    kda = db.Column(db.Float(), nullable=False)  # 场均kda值
    cs = db.Column(db.Float(), nullable=False)  # 场均补刀数
    cs_per_minute = db.Column(db.Float(), nullable=False)  # 分均补刀数
    gold = db.Column(db.Float(), nullable=False)  # 场均经济, 单位: thousand
    g_per_minute = db.Column(db.Integer(), nullable=False)  # 分均经济
    kpar = db.Column(db.Float(), nullable=False)  # 击杀参与率
    ks = db.Column(db.Float(), nullable=False)  # 击杀占比
    gs = db.Column(db.Float(), nullable=False)  # 经济占比
    cp = db.Column(db.Integer(), nullable=False)  # 英雄使用数量

    # def __repr__(self) -> str:
    #     return super().__repr__()
