from sqlalchemy.orm import session
from sqlalchemy.sql.functions import user
from app.main.service import model_save_changes, table_save_changes
import uuid
import datetime

from app.main import db
from app.main.model.pet import Pet
from app.main.model.user import User, pet_follower_table
from app.main.model.specie import Specie
from app.main.model.breed import Breed

def save_new_pet(user_pid, data):
    specie = Specie.query.filter_by(public_id=data["group_id"]).first()
    breed = Breed.query.filter_by(public_id=data["subgroup_id"]).first()
    if specie and breed:
        new_pet_pid = str(uuid.uuid4())
        new_pet = Pet(
            public_id = new_pet_pid,
            name = data.get("name"),
            bio = data.get("bio"),
            birthday = data.get("birthday"),
            sex = data.get("sex"),
            status = data.get("status"),
            is_private = data.get("is_private"),
            photo = data.get("photo"),
            registered_on = datetime.datetime.utcnow(),
            specie_group_id = data.get("group_id"),
            breed_subgroup_id = data.get("subgroup_id")
        )
        model_save_changes(new_pet)
        statement = pet_follower_table.insert().values(
            public_id = str(uuid.uuid4()),
            follower_pid = user_pid,
            pet_pid = new_pet_pid,
            is_owner = True,
            is_accepted = True
        )
        table_save_changes(statement)
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

def get_all_pets_by_user(requestor_pid, user_pid, tag_suggestions):
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
            group_id = pet[8],
            group_name = pet[9],
            subgroup_id = pet[10],
            subgroup_name = pet[11],
            is_private = pet[12],
            visitor_auth = 3 if db.session.query(
                pet_follower_table
            ).filter(
                pet_follower_table.c.follower_pid == requestor_pid
            ).filter(
                pet_follower_table.c.is_owner == True
            ).filter(
                pet_follower_table.c.pet_pid == pet[0]
            ).filter(
                pet_follower_table.c.is_accepted == True
            ).first() else 2 if db.session.query(
                pet_follower_table
            ).filter(
                pet_follower_table.c.follower_pid == requestor_pid
            ).filter(
                pet_follower_table.c.is_owner == False
            ).filter(
                pet_follower_table.c.pet_pid == pet[0]
            ).filter(
                pet_follower_table.c.is_accepted == True
            ).first() else 1 if db.session.query(
                pet_follower_table
            ).filter(
                pet_follower_table.c.follower_pid == requestor_pid
            ).filter(
                pet_follower_table.c.is_owner == False
            ).filter(
                pet_follower_table.c.pet_pid == pet[0]
            ).filter(
                pet_follower_table.c.is_accepted == False
            ).first() else 0,
            owner = [
                dict(
                    owner_id = owner[0],
                    owner_name = owner[1],
                    owner_username = owner[2],
                    owner_photo = owner[3],
                ) for owner in db.session.query(
                    User.public_id,
                    User.name,
                    User.username,
                    User.photo
                ).filter(pet_follower_table.c.follower_pid==User.public_id
                ).filter(pet_follower_table.c.is_owner==True
                ).filter(pet_follower_table.c.pet_pid==pet[0]
                ).all()
            ]
        ) for pet in db.session.query(
            Pet.public_id,
            Pet.name,
            Pet.bio,
            Pet.birthday,
            Pet.sex,
            Pet.status,
            Pet.photo,
            Pet.registered_on,
            Specie.public_id,
            Specie.name,
            Breed.public_id,
            Breed.name,
            Pet.is_private
        ).filter(
            Pet.specie_group_id == Specie.public_id
        ).filter(
            Pet.breed_subgroup_id == Breed.public_id
        ).filter(
            pet_follower_table.c.pet_pid == Pet.public_id
        ).filter(
            pet_follower_table.c.follower_pid == user_pid
        ).filter(
            pet_follower_table.c.is_owner == True if tag_suggestions == None else (True or False)
        ).filter(
            pet_follower_table.c.is_accepted == True
        ).order_by(Pet.registered_on.desc()).all()
    ]

def get_all_pets():
    return Pet.query.all()

def get_a_pet(requestor_pid, public_id):
    pet = db.session.query(
        Pet.public_id,
        Pet.name,
        Pet.bio,
        Pet.birthday,
        Pet.sex,
        Pet.status,
        Pet.photo,
        Pet.registered_on,
        Specie.public_id,
        Specie.name,
        Breed.public_id,
        Breed.name,
        Pet.is_private,
    ).filter(
        Pet.public_id == public_id
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
            group_id = pet[8],
            group_name = pet[9],
            subgroup_id = pet[10],
            subgroup_name = pet[11],
            is_private = pet[12],
            visitor_auth = 3 if db.session.query(
                pet_follower_table
            ).filter(
                pet_follower_table.c.follower_pid == requestor_pid
            ).filter(
                pet_follower_table.c.is_owner == True
            ).filter(
                pet_follower_table.c.pet_pid == public_id
            ).filter(
                pet_follower_table.c.is_accepted == True
            ).first() else 2 if db.session.query(
                pet_follower_table
            ).filter(
                pet_follower_table.c.follower_pid == requestor_pid
            ).filter(
                pet_follower_table.c.is_owner == False
            ).filter(
                pet_follower_table.c.pet_pid == public_id
            ).filter(
                pet_follower_table.c.is_accepted == True
            ).first() else 1 if db.session.query(
                pet_follower_table
            ).filter(
                pet_follower_table.c.follower_pid == requestor_pid
            ).filter(
                pet_follower_table.c.is_owner == False
            ).filter(
                pet_follower_table.c.pet_pid == public_id
            ).filter(
                pet_follower_table.c.is_accepted == False
            ).first() else 0,
            owner = [
                dict(
                    owner_id = owner[0],
                    owner_name = owner[1],
                    owner_username = owner[2],
                    owner_photo = owner[3],
                ) for owner in db.session.query(
                    User.public_id,
                    User.name,
                    User.username,
                    User.photo
                ).filter(pet_follower_table.c.follower_pid==User.public_id
                ).filter(pet_follower_table.c.is_owner==True
                ).filter(pet_follower_table.c.pet_pid==pet[0]
                ).all()
            ]
        )

def patch_a_pet(public_id, user_pid, data):
    pet = Pet.query.filter_by(public_id=public_id).first()
    if pet:
        owner = db.session.query(
            pet_follower_table
        ).filter(
            pet_follower_table.c.follower_pid == user_pid
        ).filter(
            pet_follower_table.c.pet_pid == public_id
        ).filter(
            pet_follower_table.c.is_owner == True
        ).first()

        if owner:
            pet.name = data.get("name")
            pet.bio = data.get("bio")
            pet.birthday = data.get("birthday")
            pet.sex = data.get("sex")
            pet.status = data.get("status")
            pet.photo = data.get("photo")
            pet.is_private = data.get("is_private")
            db.session.commit()

            if pet.is_private == 0:
                statement = pet_follower_table.update().where(
                    pet_follower_table.c.pet_pid==public_id
                ).where(
                    pet_follower_table.c.is_accepted == False
                ).values(
                    is_accepted = True
                )

                table_save_changes(statement)

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
        owner = db.session.query(
            pet_follower_table
        ).filter(
            pet_follower_table.c.follower_pid == user_pid
        ).filter(
            pet_follower_table.c.pet_pid == public_id
        ).filter(
            pet_follower_table.c.is_owner == True
        ).first()

        if owner and data.get("name") == pet.name:
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