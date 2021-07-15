from .. import db


class Preference(db.Model):
    __tablename__ = "preference"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    user_selector_id = db.Column(db.String, db.ForeignKey("user.public_id"), nullable=False)
    is_followed = db.Column(db.Boolean, default=True)
    breed_subgroup_id = db.Column(db.String, db.ForeignKey("breed.public_id"))
    business_type_id = db.Column(db.String, db.ForeignKey("business_type.public_id"))
    circle_type_id = db.Column(db.String, db.ForeignKey("circle_type.public_id"))

    def __repr__(self):
        return "<Preference '{}' '{}'>".format(self.user_selector_id, self.breed_subgroup_id, self.business_type_id, self.circle_type_id)