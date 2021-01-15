import uuid
import datetime

from app.main import db
from app.main.model.business import Business
from app.main.model.user import User

def save_new_business(user_pid, data):
    new_business = Business(
        public_id = str(uuid.uuid4()),
        name = data.get("name"),
        bio = data.get("bio"),
        _type = data.get("_type"),
        photo = data.get("photo"),
        registered_on = datetime.datetime.utcnow(),
        user_exec_id = user_pid,
    )
    save_changes(new_business)
    response_object = {
        'status': 'success',
        'message': 'Business successfully registered.',
        'payload': User.query.filter_by(public_id=user_pid).first().username
    }
    return response_object, 201

def get_all_businesses_by_user(user_pid):
    return [
        dict(
            id = business[0],
            name = business[1],
            bio = business[2],
            _type = business[3],
            photo = business[4],
            registered_on = business[5],
            exec_id = business[6],
            exec_name = business[7],
            exec_username = business[8],
            exec_photo = business[9]
        ) for business in db.session.query(
            Business.public_id,
            Business.name,
            Business.bio,
            Business._type,
            Business.photo,
            Business.registered_on,
            User.public_id,
            User.name,
            User.username,
            User.photo
        ).filter(
            Business.user_exec_id == user_pid
        ).filter(
            Business.user_exec_id == User.public_id
        ).order_by(Business.registered_on.desc()).all()
    ]

def patch_a_business(public_id, user_pid, data):
    business = Business.query.filter_by(public_id=public_id).first()

    if business:
        if business.user_exec_id == user_pid:
            business.name = data.get("name")
            business.bio = data.get("bio")
            business._type = data.get("_type")
            business.photo = data.get("photo")
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Business successfully updated.'
            }
            return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'No business found.'
        }
        return response_object, 404

def delete_a_business(public_id, user_pid, data):
    business = Business.query.filter_by(public_id=public_id).first()
    if business:
        if business.user_exec_id == user_pid and data.get("name") == business.name:
            db.session.delete(business)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Business successfully deleted.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Not match or no authorization.'
            }
            return response_object, 400
    else:
        response_object = {
            'status': 'fail',
            'message': 'No business found.'
        }
        return response_object, 404

def get_all_businesses():
    return Business.query.all()

def get_a_business(public_id):
    business = db.session.query(
        Business.public_id,
        Business.name,
        Business.bio,
        Business._type,
        Business.photo,
        Business.registered_on,
        User.public_id,
        User.name,
        User.username,
        User.photo
    ).filter(
        Business.public_id == public_id
    ).filter(
        Business.user_exec_id == User.public_id
    ).first()

    if business:
        return dict(
            id = business[0],
            name = business[1],
            bio = business[2],
            _type = business[3],
            photo = business[4],
            registered_on = business[5],
            exec_id = business[6],
            exec_name = business[7],
            exec_username = business[8],
            exec_photo = business[9]
        )

def save_changes(data):
    db.session.add(data)
    db.session.commit()