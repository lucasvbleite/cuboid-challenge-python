from sqlalchemy import event

from app.api.db import db
from app.api.model.cuboid import Cuboid


class Bag(db.Model):
    __tablename__ = "bags"

    id = db.Column(db.Integer, primary_key=True)
    volume = db.Column(db.Integer)
    title = db.Column(db.String(255), nullable=True)
    cuboids = db.relationship(Cuboid, backref="bag")
    payload_volume = db.Column(db.Integer, nullable=True)
    available_volume = db.Column(db.Integer, nullable=True)

    def __init__(self, volume, title, cuboids=None):
        if cuboids is None:
            cuboids = []
        self.volume = volume
        self.title = title
        self.cuboids = cuboids
        self.payload_volume = 0
        self.available_volume = self.volume


@event.listens_for(Cuboid, "after_insert")
# pylint: disable=unused-argument
def after_insert_listener(mapper, connection, target: Cuboid):
    bag = Bag.query.get(target.bag_id)
    bag.available_volume -= target.volume
    bag.payload_volume += target.volume

    table = Bag.__table__
    connection.execute(
        table.update().
        where(table.c.id == target.bag_id).
        values(available_volume=bag.available_volume, payload_volume=bag.payload_volume)
    )
