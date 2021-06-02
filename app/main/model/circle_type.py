from .. import db
from .circle import circle_type_table

class CircleType(db.Model):
    __tablename__ = "circle_type"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    circle_prop_rel = db.relationship('Circle', secondary=circle_type_table, cascade="save-update", lazy="joined")

    def __repr__(self):
        return "<CircleType '{}'>".format(self.name)