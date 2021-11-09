from flask.globals import current_app
from sqlalchemy.sql.expression import outerjoin, text
from sqlalchemy.sql.functions import func
from app.main.model.preference import Preference
from app.main.model.notification import Notification
from sqlalchemy import or_, not_
from app.main.service import model_save_changes, notification_service, table_save_changes
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
            'message': 'Pet successfully registered.'
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
            follower_count = pet[13],
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
            Pet.is_private,
            func.count(pet_follower_table.c.pet_pid).filter(pet_follower_table.c.is_owner == None).label("follower_count")
        ).select_from(
            pet_follower_table
        ).filter(
            pet_follower_table.c.follower_pid == user_pid
        ).filter(
            or_(pet_follower_table.c.is_owner == True, pet_follower_table.c.is_accepted == True) if tag_suggestions == "1" else pet_follower_table.c.is_owner == True
        ).outerjoin(
            Pet
        ).outerjoin(
            Breed
        ).outerjoin(
            Specie
        ).group_by(
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
        ).order_by(Pet.registered_on.desc()).all()
    ]

def get_all_pets_by_preference(requestor_pid, pagination_no):
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
            follower_count = pet[13],
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
            Pet.is_private,
            func.count(pet_follower_table.c.pet_pid).filter(pet_follower_table.c.is_owner == None).label("follower_count")
        ).select_from(
            Pet
        ).filter(
            not_(
                Pet.public_id.in_(
                    db.session.query(
                        pet_follower_table.c.pet_pid
                    ).select_from(
                        pet_follower_table
                    ).outerjoin(
                        Pet
                    ).outerjoin(
                        User
                    ).filter(
                        User.public_id == requestor_pid
                    ).subquery()
                )
            )
        ).outerjoin(
            Breed
        ).outerjoin(
            Specie
        ).outerjoin(
            Preference
        ).filter(
            Preference.user_selector_id == requestor_pid
        ).outerjoin(
            pet_follower_table
        ).group_by(
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
        ).order_by(
            text('follower_count DESC')
        ).paginate(
            page=pagination_no,
            per_page=current_app.config["PER_PAGE_PAGINATION"]
        ).items
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
        func.count(pet_follower_table.c.pet_pid).filter(pet_follower_table.c.is_owner == None).label("follower_count")
    ).select_from(
        Pet
    ).filter(
        Pet.public_id == public_id
    ).outerjoin(
        Breed
    ).outerjoin(
        Specie
    ).outerjoin(
        pet_follower_table
    ).group_by(
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
    ).first()

    if pet:
        notification_list = Notification.query.filter_by(
            pet_subject_id=public_id,
            user_recipient_id=requestor_pid,
            _type=0
        ).all()
        for notif in notification_list:
            notif.is_read = True
        db.session.commit()
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
            follower_count = pet[13],
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

        owner_list = db.session.query(
            pet_follower_table.c.follower_pid
        ).filter(
            pet_follower_table.c.pet_pid == public_id
        ).filter(
            pet_follower_table.c.is_owner == True
        ).all()

        if owner:
            old_pet_name = pet.name
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

            for _owner in owner_list:
                if _owner[0] != user_pid:
                    notification_service.save_new_notification(
                        "{} {} {}.".format(
                            User.query.filter_by(public_id=user_pid).first().name,
                            "has made some updates on",
                            old_pet_name
                        ),
                        0,
                        user_pid,
                        _owner[0],
                        pet_subject_id = pet.public_id
                    )

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

def delete_a_pet(public_id, user_pid, data, single_owner_removed=False):
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
                'message': 'Pet successfully deleted.',
                "single_owner_removed": 1 if single_owner_removed is True else 0
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

def get_all_by_search(requestor_pid, value, specie_pid, breed_pid, status, pagination_no):
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
            follower_count = pet[13]
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
            Pet.is_private,
            func.count(pet_follower_table.c.pet_pid).filter(pet_follower_table.c.is_owner == None).label("follower_count")
        ).select_from(
            Pet
        ).filter(
            not_(
                Pet.public_id.in_(
                    db.session.query(
                        pet_follower_table.c.pet_pid
                    ).select_from(
                        pet_follower_table
                    ).outerjoin(
                        Pet
                    ).outerjoin(
                        User
                    ).filter(
                        User.public_id == requestor_pid
                    ).subquery()
                )
            )
        ).filter(
            Pet.name.ilike("%{}%".format(value))
        ).filter(
            (Pet.specie_group_id == specie_pid) if specie_pid else (Pet.specie_group_id == Pet.specie_group_id)
        ).filter(
            (Pet.breed_subgroup_id == breed_pid) if breed_pid else (Pet.breed_subgroup_id == Pet.breed_subgroup_id)
        ).filter(
            (Pet.status == status) if status else (Pet.status == Pet.status)
        ).outerjoin(
            Breed
        ).outerjoin(
            Specie
        ).outerjoin(
            pet_follower_table
        ).group_by(
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
        ).paginate(
            page=pagination_no,
            per_page= current_app.config["PER_PAGE_PAGINATION"]
        ).items
    ]
