from app.main.model.notification import Notification
import uuid
import datetime
from app.main import db
from app.main.model.user import User
from . import model_save_changes
from sqlalchemy import func, or_

def save_new_notification(content, _type, sender_pid, recipient_pid, pet_subject_id=None, post_subject_id=None, circle_subject_id=None, business_subject_id=None):
    new_notification = Notification(
        public_id = str(uuid.uuid4()),
        content = content,
        _type = _type,
        registered_on = datetime.datetime.utcnow(),
        user_sender_id = sender_pid,
        user_recipient_id = recipient_pid,
        pet_subject_id = pet_subject_id,
        post_subject_id = post_subject_id,
        circle_subject_id = circle_subject_id,
        business_subject_id = business_subject_id
    )
    model_save_changes(new_notification)
    return new_notification.dispatch()

def get_all_notifications_by_user(requestor_pid, read=None, count=None):
    if read == "0":
        if count == "1":
            return dict(
                notif_unread_count = db.session.query(
                    func.count(Notification.public_id)
                ).filter(
                    Notification.user_recipient_id == requestor_pid
                ).filter(
                    Notification.is_read == False
                ).scalar()
            )
                
        else:
            return [
                dict(
                    public_id = notification[0],
                    content = notification[1],
                    _type = notification[2],
                    is_read = notification[3],
                    registered_on = notification[4],
                    sender_photo = notification[5],
                    recipient_id = notification[6],
                    pet_subject_id = notification[7],
                    post_subject_id = notification[8],
                    circle_subject_id = notification[9],
                    business_subject_id = notification[10]
                ) for notification in db.session.query(
                    Notification.public_id,
                    Notification.content,
                    Notification._type,
                    Notification.is_read,
                    Notification.registered_on,
                    User.photo,
                    Notification.user_recipient_id,
                    Notification.pet_subject_id,
                    Notification.post_subject_id,
                    Notification.circle_subject_id,
                    Notification.business_subject_id
                ).filter(
                    Notification.user_recipient_id == requestor_pid
                ).filter(
                    Notification.user_sender_id == User.public_id
                ).filter(
                    Notification.is_read == False
                ).order_by(Notification.registered_on.desc()).all()
            ]
    elif read == "1":
        if count == "1":
            return dict(
                notif_unread_count = db.session.query(
                    func.count(Notification.public_id)
                ).filter(
                    Notification.user_recipient_id == requestor_pid
                ).filter(
                    Notification.is_read == True
                ).scalar()
            )
        else:
            return [
                dict(
                    public_id = notification[0],
                    content = notification[1],
                    _type = notification[2],
                    is_read = notification[3],
                    registered_on = notification[4],
                    sender_photo = notification[5],
                    recipient_id = notification[6],
                    pet_subject_id = notification[7],
                    post_subject_id = notification[8],
                    circle_subject_id = notification[9],
                    business_subject_id = notification[10]
                ) for notification in db.session.query(
                    Notification.public_id,
                    Notification.content,
                    Notification._type,
                    Notification.is_read,
                    Notification.registered_on,
                    User.photo,
                    Notification.user_recipient_id,
                    Notification.pet_subject_id,
                    Notification.post_subject_id,
                    Notification.circle_subject_id,
                    Notification.business_subject_id
                ).filter(
                    Notification.user_recipient_id == requestor_pid
                ).filter(
                    Notification.user_sender_id == User.public_id
                ).filter(
                    Notification.is_read == True
                ).order_by(Notification.registered_on.desc()).all()
            ]
    elif not read:
        if count == "1":
            return dict(
                notif_unread_count = db.session.query(
                    func.count(Notification.public_id)
                ).filter(
                    Notification.user_recipient_id == requestor_pid
                ).scalar()
            )
        else:
            return [
                dict(
                    public_id = notification[0],
                    content = notification[1],
                    _type = notification[2],
                    is_read = notification[3],
                    registered_on = notification[4],
                    sender_photo = notification[5],
                    recipient_id = notification[6],
                    pet_subject_id = notification[7],
                    post_subject_id = notification[8],
                    circle_subject_id = notification[9],
                    business_subject_id = notification[10]
                ) for notification in db.session.query(
                    Notification.public_id,
                    Notification.content,
                    Notification._type,
                    Notification.is_read,
                    Notification.registered_on,
                    User.photo,
                    Notification.user_recipient_id,
                    Notification.pet_subject_id,
                    Notification.post_subject_id,
                    Notification.circle_subject_id,
                    Notification.business_subject_id
                ).filter(
                    Notification.user_recipient_id == requestor_pid
                ).filter(
                    Notification.user_sender_id == User.public_id
                ).order_by(Notification.registered_on.desc()).all()
            ]

def get_a_notification(requestor_pid, public_id):
    notification = db.session.query(
        Notification.public_id,
        Notification.content,
        Notification._type,
        Notification.is_read,
        Notification.registered_on,
        User.photo,
        Notification.user_recipient_id,
        Notification.pet_subject_id,
        Notification.post_subject_id,
        Notification.circle_subject_id,
        Notification.business_subject_id
    ).filter(
        Notification.user_sender_id == User.public_id
    ).first()

    if notification:
        return dict(
            public_id = notification[0],
            content = notification[1],
            _type = notification[2],
            is_read = notification[3],
            registered_on = notification[4],
            sender_photo = notification[5],
            recipient_id = notification[6],
            pet_subject_id = notification[7],
            post_subject_id = notification[8],
            circle_subject_id = notification[9],
            business_subject_id = notification[10]
        )
