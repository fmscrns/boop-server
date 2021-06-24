from app.main.service import model_save_changes
import uuid
import datetime
from app.main import db
from app.main.model.circle_type import CircleType

def save_new_circleType(data):
    circle_type = CircleType.query.filter_by(name=data['name']).first()
    if not circle_type:
        new_circleType = CircleType(
            public_id=str(uuid.uuid4()),
            name=data["name"],
            registered_on=datetime.datetime.utcnow()
        )
        model_save_changes(new_circleType)
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