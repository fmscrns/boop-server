from .. import db
import os, requests, json
from flask import current_app
from app.main.model.user import User
from itsdangerous import URLSafeTimedSerializer

# when is notification read:
# (1) USER COMMENT ON POST
#   (a) post page visit
#   (b) the temporary alert is clicked
#   (c) the navbar notif dropdown item is clicked
# (2) USER LIKE ON POST
#   (a) post page visit
#   (b) the temporary alert is clicked
#   (c) the navbar notif dropdown item is clicked
# (2) USER FOLLOW ON PET
#   (a) pet member page visit
#   (b) the temporary alert is clicked
#   (c) the navbar notif dropdown item is clicked
# (2) USER REQUEST TO FOLLOW ON PET
#   (a) pet pending followers page visit
#   (b) the temporary alert is clicked
#   (c) the navbar notif dropdown item is clicked
# (2) USER REQUEST TO JOIN ON CIRCLE
#   (a) circle pending members page visit
#   (b) the temporary alert is clicked
#   (c) the navbar notif dropdown item is clicked
# (2) USER FOLLOW ON BUSINESS
#   (a) business followers page visit
#   (b) the temporary alert is clicked
#   (c) the navbar notif dropdown item is clicked

class Notification                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         (db.Model):
    __tablename__ = "notification"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.String(400), nullable=False)
    _type = db.Column(db.Integer, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    user_sender_id = db.Column(db.String, db.ForeignKey("user.public_id"), nullable=False)
    user_recipient_id = db.Column(db.String, db.ForeignKey("user.public_id"), nullable=False)
    user_sender = db.relationship("User", foreign_keys="Notification.user_sender_id")
    user_recipient = db.relationship("User", foreign_keys="Notification.user_recipient_id")

    pet_subject_id = db.Column(db.String, db.ForeignKey("pet.public_id"))
    post_subject_id = db.Column(db.String, db.ForeignKey("post.public_id"))
    circle_subject_id = db.Column(db.String, db.ForeignKey("circle.public_id"))
    business_subject_id = db.Column(db.String, db.ForeignKey("business.public_id"))

    def __repr__(self):
        return "<Notification '{}'>".format(self.public_id)

    def dispatch(self):
        serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY"))
        token = serializer.dumps(dict(
            public_id = self.public_id,
            content = self.content,
            _type = self._type,
            is_read = self.is_read,
            sender_photo = User.query.filter_by(public_id=self.user_sender_id).first().photo,
            recipient_username = User.query.filter_by(public_id=self.user_recipient_id).first().username,
            pet_subject_id = self.pet_subject_id,
            post_subject_id = self.post_subject_id,
            circle_subject_id = self.circle_subject_id,
            business_subject_id = self.business_subject_id
        ), salt="new-notif")

        return requests.post("{}/notification/receiver".format(
            current_app.config["MAIN_DOMAIN"]),
            json = {
                "token": token
            }
        )