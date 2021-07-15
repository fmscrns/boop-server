from .. import db
from .user import pet_follower_table
import datetime
# status 0 - closed
# status 1 - open for adoption
# status 2 - deceased

post_subject_table = db.Table('post_subject_table',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('public_id', db.String(100), unique=True),
    db.Column('post_pid', db.String(100), db.ForeignKey('post.public_id')),
    db.Column('subject_pid', db.String(100), db.ForeignKey('pet.public_id')),
    db.Column('registered_on', db.DateTime, nullable=False, default=datetime.datetime.utcnow)
)

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
    is_private = db.Column(db.Integer, nullable=False, default=0)

    specie_group_id = db.Column(db.String, db.ForeignKey("specie.public_id"), nullable=False)
    breed_subgroup_id = db.Column(db.String, db.ForeignKey("breed.public_id"), nullable=False)
    user_follower_rel = db.relationship('User', secondary=pet_follower_table, cascade="save-update", lazy="joined")
    post_subject_rel = db.relationship('Post', secondary=post_subject_table, cascade="save-update", lazy="joined")
    notification_subject_rel = db.relationship("Notification", cascade="all,delete", lazy="joined")

    def __repr__(self):
        return "<Pet '{}'>".format(self.name)