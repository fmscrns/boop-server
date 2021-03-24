import uuid
import datetime

from app.main import db
from app.main.model.business_type import BusinessType


def save_new_businessType(data):
    business_type = BusinessType.query.filter_by(name=data['name']).first()
    if not business_type:
        new_businessType = BusinessType(
            public_id=str(uuid.uuid4()),
            name=data["name"],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_businessType)
        response_object = {
            'status': 'success',
            'message': 'Business type successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Business type already exists.',
        }
        return response_object, 409

def patch_a_businessType(public_id, data):
    business_type = BusinessType.query.filter_by(public_id=public_id).first()
    if business_type:
        business_type.name = data["name"]
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Business type successfully updated.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'No business type found.'
        }
        return response_object, 404

def delete_a_businessType(public_id, data):
    business_type = BusinessType.query.filter_by(public_id=public_id).first()

    if business_type and data["name"] == business_type.name:
        db.session.delete(business_type)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Business type successfully deleted.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'No business type found or name not match.'
        }
        return response_object, 404

def get_all_businessTypes():
    return BusinessType.query.all()

def get_a_businessType(public_id):
    return BusinessType.query.filter_by(public_id=public_id).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()
