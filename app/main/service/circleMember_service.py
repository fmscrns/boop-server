import uuid
import datetime

from app.main import db
from app.main.model.circle_member import CircleMember
from app.main.model.circle import Circle


def new_member(user_pid, public_id):
    new_public_id = str(uuid.uuid4())

    circle = Circle.query.filter_by(public_id=public_id).first()
    if not circle_member:
        new_c_member = CircleMember(
            public_id = new_public_id,
            registered_on = datetime.datetime.utcnow(),
            join_by = user_pid,
            circle_membership_id = circle.public_id
        )
        save_changes(new_c_member)
        response_object = {
            'status': 'success',
            'message': 'Circle type successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Circle type already exists.',
        }
        return response_object, 409

def patch_a_circleType(public_id, data):
    circle_type = CircleType.query.filter_by(public_id=public_id).first()
    if circle_type:
        circle_type.name = data["name"]
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Circle type successfully updated.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'No circle type found.'
        }
        return response_object, 404

def delete_a_circleType(public_id, data):
    circle_type = CircleType.query.filter_by(public_id=public_id).first()

    if circle_type and data["name"] == circle_type.name:
        db.session.delete(circle_type)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Circle type successfully deleted.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'No circle type found or name not match.'
        }
        return response_object, 404

def get_all_circleTypes():
    return CircleType.query.all()

def get_a_circleType(public_id):
    return CircleType.query.filter_by(public_id=public_id).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()
