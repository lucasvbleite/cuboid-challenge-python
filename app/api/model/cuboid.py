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

    def create_cuboid(self, bag_available_volume):
        if self.volume <= bag_available_volume:
            db.session.add(self)
            db.session.commit()
            return self
        return None

    def update_cuboid(self, width=None, depth=None, height=None):
        if depth:
            self.depth = depth
        if width:
            self.width = width
        if height:
            self.height = height
        self.volume = self.height * self.width * self.depth
        db.session.commit()
        return self
