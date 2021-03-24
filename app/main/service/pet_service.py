import uuid
import datetime

from app.main import db
from app.main.model.pet import Pet
from app.main.model.user import User
from app.main.model.specie import Specie
from app.main.model.breed import Breed

def save_new_pet(user_pid, data):
    specie = Specie.query.filter_by(public_id=data["group_id"]).first()
    breed = Breed.query.filter_by(public_id=data["subgroup_id"]).first()
    if specie and breed:
        new_pet = Pet(
            public_id = str(uuid.uuid4()),
            name = data.get("name"),
            bio = data.get("bio"),
            birthday = data.get("birthday"),
            sex = data.get("sex"),
            status = data.get("status"),
            photo = data.get("photo"),
            registered_on = datetime.datetime.utcnow(),
            user_owner_id = user_pid,
            specie_group_id = data.get("group_id"),
            breed_subgroup_id = data.get("subgroup_id")
        )
        save_changes(new_pet)
        response_object = {
            'status': 'success',
            'message': 'Pet successfully registered.',
            'payload': User.query.filter_by(public_id=user_pid).first().username
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Bad request.',
        }
        return response_object, 400

def get_all_pets_by_user(user_pid):
    return [
        dict(
            public_id = pet[0],
            name = pet[1],
            bio = pet[2],
            birthday = pet[3],
            sex = pet[4],
            status = pet[5],
            photo = pet[6],
            registered_on = pet[7],
            owner_id = pet[8],
            owner_name = pet[9],
            owner_username = pet[10],
            owner_photo = pet[11],
            group_id = pet[12],
            group_name = pet[13],
            subgroup_id = pet[14],
            subgroup_name = pet[15]
        ) for pet in db.session.query(
            Pet.public_id,
            Pet.name,
            Pet.bio,
            Pet.birthday,
            Pet.sex,
            Pet.status,
            Pet.photo,
            Pet.registered_on,
            User.public_id,
            User.name,
            User.username,
            User.photo,
            Specie.public_id,
            Specie.name,
            Breed.public_id,
            Breed.name
        ).filter(
            Pet.user_owner_id == user_pid
        ).filter(
            Pet.user_owner_id == User.public_id
        ).filter(
            Pet.specie_group_id == Specie.public_id
        ).filter(
            Pet.breed_subgroup_id == Breed.public_id
        ).order_by(Pet.registered_on.desc()).all()
    ]

def get_all_pets():
    return Pet.query.all()

def get_a_pet(public_id):
    pet = db.session.query(
        Pet.public_id,
        Pet.name,
        Pet.bio,
        Pet.birthday,
        Pet.sex,
        Pet.status,
        Pet.photo,
        Pet.registered_on,
        User.public_id,
        User.name,
        User.username,
        User.photo,
        Specie.public_id,
        Specie.name,
        Breed.public_id,
        Breed.name
    ).filter(
        Pet.public_id == public_id
    ).filter(
        Pet.user_owner_id == User.public_id
    ).filter(
        Pet.specie_group_id == Specie.public_id
    ).filter(
        Pet.breed_subgroup_id == Breed.public_id
    ).first()

    if pet:
        return dict(
            public_id = pet[0],
            name = pet[1],
            bio = pet[2],
            birthday = pet[3],
            sex = pet[4],
            status = pet[5],
            photo = pet[6],
            registered_on = pet[7],
            owner_id = pet[8],
            owner_name = pet[9],
            owner_username = pet[10],
            owner_photo = pet[11],
            group_id = pet[12],
            group_name = pet[13],
            subgroup_id = pet[14],
            subgroup_name = pet[15]
        )

def patch_a_pet(public_id, user_pid, data):
    pet = Pet.query.filter_by(public_id=public_id).first()

    if pet:
        if pet.user_owner_id == user_pid:
            pet.name = data.get("name")
            pet.bio = data.get("bio")
            pet.birthday = data.get("birthday")
            pet.sex = data.get("sex")
            pet.status = data.get("status")
            pet.photo = data.get("photo")
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Pet successfully updated.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'No authorization.'
            }
            return response_object, 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'No pet found.'
        }
        return response_object, 404

def delete_a_pet(public_id, user_pid, data):
    pet = Pet.query.filter_by(public_id=public_id).first()
    if pet:
        if pet.user_owner_id == user_pid and data.get("name") == pet.name:
            db.session.delete(pet)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Pet successfully deleted.'
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
            'message': 'No pet found.'
        }
        return response_object, 404

def save_changes(data):
    db.session.add(data)
    db.session.commit()