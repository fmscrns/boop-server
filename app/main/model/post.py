from .. import db
from .pet import post_subject_table

class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.String(400))
    photo = db.Column(db.String(50))
    registered_on = db.Column(db.DateTime, nullable=False)

    user_creator_id = db.Column(db.String, db.ForeignKey("user.public_id"), nullable=False)
    business_pinboard_id = db.Column(db.String, db.ForeignKey("business.public_id"))
    circle_confiner_id = db.Column(db.String, db.ForeignKey("circle.public_id"))
    post_subject_rel = db.relationship('Pet', secondary=post_subject_table, cascade="save-update", lazy="joined")

    def __repr__(self):
        return "<Post '{}'>".format(self.public_id)