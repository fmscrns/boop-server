import uuid
import datetime

from app.main import db
from app.main.model.breed import Breed
from app.main.model.specie import Specie


def save_new_breed(data):
    breed = Breed.query.filter_by(name=data['name']).first()
    specie = Specie.query.filter_by(public_id=data["parent_id"]).first()
    if not breed and specie:
        new_breed = Breed(
            public_id=str(uuid.uuid4()),
            name=data["name"],
            specie_parent_id=data["parent_id"],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_breed)
        response_object = {
            'status': 'success',
            'message': 'Breed successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Breed already exists or specie does not exist.',
        }
        return response_object, 409

def patch_a_breed(public_id, data):
    breed = Breed.query.filter_by(public_id=public_id).first()

    breed.name = data["name"]
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Breed successfully updated.'
    }
    return response_object, 201

def delete_a_breed(public_id, data):
    breed = Breed.query.filter_by(public_id=public_id).first()

    if data["name"] == breed.name:
        db.session.delete(breed)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Breed successfully deleted.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Not match.'
        }
        return response_object, 400

def get_all_breeds():
    breeds = [
        dict(
            public_id = breed[0],
            name = breed[1],
            parent_id = breed[2],
            parent_name = breed[3]
        ) for breed in db.session.query(
            Breed.public_id,
            Breed.name,
            Specie.public_id,
            Specie.name
        ).filter(
            Breed.specie_parent_id == Specie.public_id
        ).all()
    ]
    if breeds:
        return breeds
    return 404

def get_a_breed(public_id):
    return Breed.query.filter_by(public_id=public_id).first()

def get_all_by_specie(specie_id):
    return Breed.query.filter_by(specie_parent_id=specie_id).all()

def save_changes(data):
    db.session.add(data)
    db.session.commit()