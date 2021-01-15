from .. import db

# status 0 - closed
# status 1 - open for adoption
# status 2 - deceased

class Pet(db.Model):
    __tablename__ = "pet"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.String(100))
    birthday = db.Column(db.DateTime)
    sex = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(50))
    registered_on = db.Column(db.DateTime, nullable=False)

    user_owner_id = db.Column(db.String, db.ForeignKey("user.public_id"), nullable=False)
    specie_group_id = db.Column(db.String, db.ForeignKey("specie.public_id"), nullable=False)
    breed_subgroup_id = db.Column(db.String, db.ForeignKey("breed.public_id"), nullable=False)
    
    def __repr__(self):
        return "<Pet '{}'>".format(self.name)