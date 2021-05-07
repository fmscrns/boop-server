from datetime import datetime
from .. import db

circle_type_table = db.Table('circle_type_table',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('public_id', db.String(100), unique=True),
    db.Column('circle_pid', db.String(100), db.ForeignKey('circle.public_id')),
    db.Column('type_pid', db.String(100), db.ForeignKey('circle_type.public_id')),
    db.Column('registered_on', db.DateTime, nullable=False, default=datetime.utcnow)
)

# circle_membership_table = db.Table('circle_membership_table',
#     db.Column('id', db.Integer, primary_key=True, autoincrement=True),
#     db.Column('public_id', db.String(100), unique=True),
#     db.Column('circle_pid', db.String(100), db.ForeignKey('circle.public_id')),
#     db.Column('membership_pid', db.String(100), db.ForeignKey('circle_type.public_id')),
#     db.Column('registered_on', db.DateTime, nullable=False, default=datetime.utcnow)
# )

class Circle(db.Model):
    __tablename__ = "circle"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    bio = db.Column(db.String(100))
    photo = db.Column(db.String(50))

    user_admin_id = db.Column(db.String, db.ForeignKey("user.public_id"), nullable=False) 

    prop_circle_rel = db.relationship('CircleType', secondary=circle_type_table, lazy="joined")
    #prop_membership_rel = db.relationship('CircleMembership', secondary=circle_membership_table, lazy="joined")
    
    def __repr__(self):
        return "<Circle '{}'>".format(self.name)