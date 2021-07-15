from app.main.service import user_service
from sqlalchemy.sql.expression import outerjoin
from app.main.model.breed import Breed
from sqlalchemy.sql.functions import func
from app.main.model.preference import Preference
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
    if specie:
        specie.name = data["name"]
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Specie successfully updated.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'No specie found.'
        }
        return response_object, 404

def delete_a_specie(public_id, data):
    specie = Specie.query.filter_by(public_id=public_id).first()

    if specie and data["name"] == specie.name:
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
            'message': 'No specie found or name not match.'
        }
        return response_object, 404

def get_all_species(requestor_pid):
    return [
        dict(
            public_id = specie[0],
            name = specie[1],
            is_preferred = specie[2]
        ) for specie in db.session.query(
            Specie.public_id,
            Specie.name,
            func.count(Preference.user_selector_id).filter(Preference.user_selector_id==requestor_pid).filter(Preference.is_followed==True)
        ).select_from(
            Specie
        ).outerjoin(
            Breed
        ).outerjoin(
            Preference
        ).group_by(
            Specie.public_id,
            Specie.name
        ).all()
    ]

def get_a_specie(public_id):
    return Specie.query.filter_by(public_id=public_id).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()
