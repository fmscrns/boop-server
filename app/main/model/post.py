from .. import db
from .pet import post_subject_table
from .user import post_liker_table

class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.String(400), nullable=False)
    photo_1 = db.Column(db.String(50))
    photo_2 = db.Column(db.String(50))
    photo_3 = db.Column(db.String(50))
    photo_4 = db.Column(db.String(50))
    registered_on = db.Column(db.DateTime, nullable=False)

    user_creator_id = db.Column(db.String, db.ForeignKey("user.public_id"), nullable=False)
    business_pinboard_id = db.Column(db.String, db.ForeignKey("business.public_id"))
    circle_confiner_id = db.Column(db.String, db.ForeignKey("circle.public_id"))
    post_subject_rel = db.relationship('Pet', secondary=post_subject_table, cascade="save-update", lazy="joined")
    post_liker_rel = db.relationship('User', secondary=post_liker_table, cascade="save-update", lazy="joined")
    comment_parent_rel = db.relationship("Comment", cascade="all,delete", lazy="joined")

    def __repr__(self):
        return "<Post '{}'>".format(self.public_id)