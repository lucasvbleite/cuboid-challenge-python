from app.api.db import db


class Cuboid(db.Model):
    __tablename__ = "cuboids"

    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    depth = db.Column(db.Integer)
    bag_id = db.Column(db.Integer, db.ForeignKey("bags.id"), nullable=False)

    def __init__(self, width, height, depth, bag_id):
        self.width = width
        self.height = height
        self.depth = depth
        self.bag_id = bag_id
        self.volume = self.width * self.height * self.depth
