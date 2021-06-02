from app.main.service import model_save_changes
import uuid
import datetime

from app.main import db
from app.main.model.breed import Breed
from app.main.model.specie import Specie
from app.main.model.pet import Pet

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
        model_save_changes(new_breed)
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
    specie = Specie.query.filter_by(public_id=data["parent_id"]).first()

    if breed and specie:
        breed.name = data["name"]
        breed.specie_parent_id = data["parent_id"]
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Breed successfully updated.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'No breed or specie found.'
        }
        return response_object, 404

def delete_a_breed(public_id, data):
    breed = Breed.query.filter_by(public_id=public_id).first()
    specie = Specie.query.filter_by(public_id=data["parent_id"]).first()
    pet = Pet.query.filter_by(breed_subgroup_id=breed.public_id).first()

    if breed and specie:
        if breed.specie_parent_id==specie.public_id:
            if data["name"] == breed.name and not pet:
                db.session.delete(breed)
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'message': 'Breed successfully deleted.'
                }
                return response_object, 201
            elif pet:
                response_object = {
                    'status': 'fail',
                    'message': 'User created pets depend on this breed.'
                }
                return response_object, 405
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Not match.'
                }
                return response_object, 400
        else:
            response_object = {
                'status': 'fail',
                'message': 'Bad request.'
            }
            return response_object, 400
    else:
        response_object = {
            'status': 'fail',
            'message': 'No breed or specie found.'
        }
        return response_object, 404

def get_all_breeds():
    return [
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

def get_a_breed(public_id):
    breed = db.session.query(
        Breed.public_id,
        Breed.name,
        Specie.public_id,
        Specie.name
    ).filter(
        Breed.specie_parent_id == Specie.public_id
    ).first()

    return dict(
        public_id = breed[0],
        name = breed[1],
        parent_id = breed[2],
        parent_name = breed[3]
    ) if breed else {
        'status': 'fail',
        'message': 'No breed found.'
    }, 404

def get_all_by_specie(specie_id):
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
        ).filter(
            Specie.public_id == specie_id
        ).all()
    ]
    if breeds:
        return breeds
    return {
        'status': 'fail',
        'message': 'No breeds found.'
    }, 404