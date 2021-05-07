from datetime import datetime
from .. import db

circle_mem_rel = db.Table("circle_membership_rel",
    db.Column("circle_id", db.String, db.ForeignKey("circle.public_id", ondelete="cascade")),
    db.Column("user_m_id", db.String, db.ForeignKey("user.public_id", ondelete="cascade"))
)

class Member(db.Model):
    __tablename__ = "member"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    user_membership_id = db.Column(db.String, db.ForeignKey("user.public_id"), nullable=False) 
    circle_membership_id = db.Column(db.String, db.ForeignKey("circle.public_id"), nullable=False)

    circle_rel = db.relationship("Circle", secondary=circle_mem_rel, backref=db.backref("circle", lazy=True), cascade="all, delete", passive_deletes=True)
    

    def __repr__(self):
        return "<Member '{}'>".format(self.name)