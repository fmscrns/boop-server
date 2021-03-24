from .. import db


class Specie(db.Model):
    __tablename__ = "specie"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    breed_parent_rel = db.relationship("Breed", cascade="all,delete", lazy="joined")

    def __repr__(self):
        return "<Specie '{}'>".format(self.name)