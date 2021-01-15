from .. import db

# type 0 - grooming
# type 1 - veterinarian
# type 2 - supply and accessories
# type 3 - type 0 and type 1
# type 4 - type 0 and type 2
# type 5 - type 1 and type 2
# type 6 - all

class Business(db.Model):
    __tablename__ = "business"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    _type = db.Column(db.Integer, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    bio = db.Column(db.String(100))
    photo = db.Column(db.String(50))

    user_exec_id = db.Column(db.String, db.ForeignKey("user.public_id"), nullable=False)
    
    def __repr__(self):
        return "<Business '{}'>".format(self.name)