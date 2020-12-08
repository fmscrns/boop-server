from .. import db


class Breed(db.Model):
    __tablename__ = "breed"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    specie_parent_id = db.Column(db.String, db.ForeignKey("specie.public_id"), nullable=False)

    def __repr__(self):
        return "<Breed '{}'>".format(self.name)