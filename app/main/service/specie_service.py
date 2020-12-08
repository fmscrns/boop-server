import uuid
import datetime

from app.main import db
from app.main.model.specie import Specie


def save_new_specie(data):
    specie = Specie.query.filter_by(name=data['name']).first()
    if not specie:
        new_specie = Specie(
            public_id=str(uuid.uuid4()),
            name=data["name"],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_specie)
        response_object = {
            'status': 'success',
            'message': 'Specie successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Specie already exists.',
        }
        return response_object, 409

def patch_a_specie(public_id, data):
    specie = Specie.query.filter_by(public_id=public_id).first()

    specie.name = data["name"]
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Specie successfully updated.'
    }
    return response_object, 201

def delete_a_specie(public_id, data):
    specie = Specie.query.filter_by(public_id=public_id).first()

    if data["name"] == specie.name:
        db.session.delete(specie)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Specie successfully deleted.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Not match.'
        }
        return response_object, 400

def get_all_species():
    return Specie.query.all()

def get_a_specie(public_id):
    return Specie.query.filter_by(public_id=public_id).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()
