from apps import db


class PlayerInfo(db.Model):
    __tablename__ = "PlayerInfo"

    name = db.Column(db.String(30), primary_key=True)
    id = db.Column(db.String(30), nullable=False)
    birthday = db.Column(db.String(50), nullable=False)
    residency = db.Column(db.String(30), nullable=False)
