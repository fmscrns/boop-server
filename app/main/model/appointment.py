from .. import db

class Appointment(db.Model):
    __tablename__ = "appointment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(100))
    user_client_id = db.Column(db.String, db.ForeignKey("user.public_id"), nullable=False)
    pet_appointee_id = db.Column(db.String, db.ForeignKey("pet.public_id"), nullable=False)
    business_service_id = db.Column(db.String, db.ForeignKey("business.public_id"), nullable=False)
    
    def __repr__(self):
        return "<Appointment '{}'>".format(self.name)