from .. import db

class BusinessOperation(db.Model):
    __tablename__ = "business_operation"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    day = db.Column(db.String(20), nullable=False)
    is_open = db.Column(db.Boolean, nullable=False)
    start_at = db.Column(db.Time)
    end_at = db.Column(db.Time)

    business_prop_id = db.Column(db.String, db.ForeignKey("business.public_id"), nullable=False)
    
    def __repr__(self):
        return "<BusinessOperation '{}'>".format(self.name)