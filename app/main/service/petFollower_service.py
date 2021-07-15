from app.main.model.notification import Notification
from app.main.service import notification_service, table_save_changes
import uuid
from app.main import db
from app.main.model.pet import Pet
from app.main.model.user import User, pet_follower_table
from .pet_service import delete_a_pet
from sqlalchemy import func

from app.main.service import pet_service

def create_pet_follower(user_pid, pet_pid):
    pet = Pet.query.filter_by(public_id=pet_pid).first()
    if pet:
        follower = db.session.query(
            pet_follower_table
        ).filter(
            pet_follower_table.c.follower_pid == user_pid
        ).filter(
            pet_follower_table.c.pet_pid == pet_pid
        ).first()

        owner_list = db.session.query(
            pet_follower_table.c.follower_pid
        ).filter(
            pet_follower_table.c.pet_pid == pet_pid
        ).filter(
            pet_follower_table.c.is_owner == True
        ).all()

        if not follower:
            statement = pet_follower_table.insert().values(
                public_id=str(uuid.uuid4()),
                follower_pid=user_pid,
                pet_pid=pet_pid,
                is_accepted=(True if pet.is_private == 0 else False)
            )
            table_save_changes(statement)

            for owner in owner_list:
                notification_service.save_new_notification(
                    "{} {} {}.".format(
                        User.query.filter_by(public_id=user_pid).first().name,
                        "followed" if pet.is_private == 0 else "has requested to follow",
                        pet.name
                    ),
                    pet.is_private,
                    user_pid,
                    owner[0],
                    pet_subject_id = pet.public_id
                )

            response_object = {
                'status': 'success',
                'message': 'Pet successfully followed.' if pet.is_private == 0 else "Awaiting owner's approval."
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Pet already followed.',
            }
            return response_object, 409
    else:
        response_object = {
            'status': 'fail',
            'message': 'No pet found.'
        }
        return response_object, 404

def get_all_pet_followers(requestor_pid, pet_pid, type):
    pet = Pet.query.filter_by(public_id=pet_pid).first()
    requesting_owner = db.session.query(
        pet_follower_table
    ).filter(
        pet_follower_table.c.follower_pid == requestor_pid
    ).filter(
        pet_follower_table.c.pet_pid == pet_pid
    ).filter(
        pet_follower_table.c.is_owner == True
    ).first()
    if pet:
        if (requesting_owner is not None and type == "0") or (type == "1"):
            if type == "0":
                notification_list = Notification.query.filter_by(
                    pet_subject_id=pet_pid,
                    user_recipient_id=requestor_pid,
                    _type=1
                ).all()
                for notif in notification_list:
                    notif.is_read = True
                db.session.commit()
            return db.session.query(
                User
            ).filter(
                pet_follower_table.c.pet_pid == pet_pid
            ).filter(
                pet_follower_table.c.follower_pid == User.public_id
            ).filter(
                pet_follower_table.c.is_accepted == (False if type == "0" else True)
            ).filter(
                pet_follower_table.c.is_owner == False
            ).all()
        else:
            response_object = {
                'status': 'fail',
                'message': 'Forbidden.'
            }
            return response_object, 403
    else:
        response_object = {
            'status': 'fail',
            'message': 'No pet found.'
        }
        return response_object, 404

def create_pet_owner(user_pid, pet_pid, data):
    pet = Pet.query.filter_by(public_id=pet_pid).first()
    if pet:
        user = User.query.filter_by(public_id=data.get("public_id")).first()
        admin = db.session.query(
            pet_follower_table
        ).filter(
            pet_follower_table.c.follower_pid == user_pid
        ).filter(
            pet_follower_table.c.pet_pid == pet_pid
        ).filter(
            pet_follower_table.c.is_owner == True
        ).first()

        if user and admin:
            follower = db.session.query(
                pet_follower_table
            ).filter(
                pet_follower_table.c.follower_pid == data.get("public_id")
            ).filter(
                pet_follower_table.c.pet_pid == pet_pid
            ).first()

            if follower:
                if follower[4] == False:
                    statement = pet_follower_table.update().where(
                        pet_follower_table.c.follower_pid==data.get("public_id")
                    ).where(
                        pet_follower_table.c.pet_pid==pet_pid
                    ).values(
                        is_owner = True,
                        is_accepted = True
                    )
                    table_save_changes(statement)

                    notification_service.save_new_notification(
                        "{} has made you an owner of {}.".format(
                            User.query.filter_by(public_id=user_pid).first().name,
                            pet.name
                        ),
                        0,
                        user_pid,
                        data.get("public_id"),
                        pet_subject_id = pet_pid
                    )

                    response_object = {
                        'status': 'success',
                        'message': 'Pet successfully have new owner.'
                    }
                    return response_object, 201
                else:
                    response_object = {
                        'status': 'fail',
                        'message': 'User is already an owner of the pet.',
                    }
                    return response_object, 409
            else:
                statement = pet_follower_table.insert().values(
                    public_id=str(uuid.uuid4()),
                    follower_pid=data.get("public_id"),
                    pet_pid=pet_pid,
                    is_accepted=True,
                    is_owner=True
                )
                table_save_changes(statement)
                response_object = {
                    'status': 'success',
                    'message': 'Pet successfully have new owner.'
                }
                return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Forbidden.',
            }
            return response_object, 403
    else:
        response_object = {
            'status': 'fail',
            'message': 'No pet found.'
        }
        return response_object, 404

def delete_pet_owner(user_pid, pet_pid, owner_id, data):
    pet = Pet.query.filter_by(public_id=pet_pid).first()
    if pet:
        requestor = db.session.query(
            pet_follower_table
        ).filter(
            pet_follower_table.c.follower_pid == user_pid
        ).filter(
            pet_follower_table.c.pet_pid == pet_pid
        ).filter(
            pet_follower_table.c.is_owner == True
        ).first()

        target_owner = db.session.query(
            pet_follower_table
        ).filter(
            pet_follower_table.c.follower_pid == owner_id
        ).filter(
            pet_follower_table.c.pet_pid == pet_pid
        ).filter(
            pet_follower_table.c.is_owner == True
        ).first()

        owner_list_length = db.session.query(
            func.count(pet_follower_table.c.public_id)
        ).filter(
            pet_follower_table.c.pet_pid == pet_pid
        ).filter(
            pet_follower_table.c.is_owner == True
        ).scalar()
        if requestor and target_owner:
            if owner_list_length != 1:
                statement = pet_follower_table.update().where(
                    pet_follower_table.c.follower_pid==owner_id
                ).where(
                    pet_follower_table.c.pet_pid==pet_pid
                ).values(
                    is_owner = False
                )
                table_save_changes(statement)

                notification_service.save_new_notification(
                    "{} has removed you as owner of {}.".format(
                        User.query.filter_by(public_id=user_pid).first().name,
                        pet.name
                    ),
                    0,
                    user_pid,
                    owner_id,
                    pet_subject_id = pet_pid
                )

                response_object = {
                    'status': 'success',
                    'message': 'Pet owner successfully removed.',
                    'single_owner_removed': 0
                }
                return response_object, 201
            else:
                return pet_service.delete_a_pet(pet_pid, user_pid, data, single_owner_removed=True)
        else:
            response_object = {
                'status': 'fail',
                'message': 'Forbidden.',
            }
            return response_object, 403
    else:
        response_object = {
            'status': 'fail',
            'message': 'No pet found.'
        }
        return response_object, 404

def delete_pet_follower(user_pid, pet_pid, follower_pid):
    pet = Pet.query.filter_by(public_id=pet_pid).first()
    if pet:
        requestor = db.session.query(
            pet_follower_table
        ).filter(
            pet_follower_table.c.follower_pid == user_pid
        ).filter(
            pet_follower_table.c.pet_pid == pet_pid
        ).first()

        target_follower = db.session.query(
            pet_follower_table
        ).filter(
            pet_follower_table.c.follower_pid == follower_pid
        ).filter(
            pet_follower_table.c.pet_pid == pet_pid
        ).filter(
            pet_follower_table.c.is_owner == False
        ).first()

        if requestor and target_follower:
            owner = db.session.query(
                pet_follower_table
            ).filter(
                pet_follower_table.c.follower_pid == user_pid
            ).filter(
                pet_follower_table.c.pet_pid == pet_pid
            ).filter(
                pet_follower_table.c.is_owner == True
            ).first()

            if owner:
                statement = pet_follower_table.delete().where(
                    pet_follower_table.c.follower_pid==follower_pid
                ).where(
                    pet_follower_table.c.pet_pid==pet_pid
                )
                table_save_changes(statement)
                response_object = {
                        'status': 'success',
                        'message': 'Pet follower successfully deleted.'
                    }
                return response_object, 201
            elif user_pid == follower_pid:
                statement = pet_follower_table.delete().where(
                    pet_follower_table.c.follower_pid==follower_pid
                ).where(
                    pet_follower_table.c.pet_pid==pet_pid
                )
                table_save_changes(statement)
                response_object = {
                        'status': 'success',
                        'message': 'Pet follower successfully deleted.'
                    }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Request unauthorized.'
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'User is not following this pet.',
            }
            return response_object, 404

def accept_pet_follower(user_pid, pet_pid, follower_pid):
    pet = Pet.query.filter_by(public_id=pet_pid).first()
    if pet:
        owner = db.session.query(
            pet_follower_table
        ).filter(
            pet_follower_table.c.follower_pid == user_pid
        ).filter(
            pet_follower_table.c.pet_pid == pet_pid
        ).filter(
            pet_follower_table.c.is_owner == True
        ).first()

        follower = db.session.query(
            pet_follower_table
        ).filter(
            pet_follower_table.c.follower_pid == follower_pid
        ).filter(
            pet_follower_table.c.pet_pid == pet_pid
        ).filter(
            pet_follower_table.c.is_accepted == False
        ).first()

        if owner:
            if follower:
                statement = pet_follower_table.update().where(
                    pet_follower_table.c.follower_pid==follower_pid
                ).where(
                    pet_follower_table.c.pet_pid==pet_pid
                ).values(
                    is_accepted = True
                )
                table_save_changes(statement)

                notification_service.save_new_notification(
                    "{} has accepted your request to follow on {}.".format(
                        User.query.filter_by(public_id=user_pid).first().name,
                        pet.name
                    ),
                    0,
                    user_pid,
                    follower_pid,
                    pet_subject_id = pet.public_id
                )

                response_object = {
                    'status': 'success',
                    'message': 'Pet follower successfully accepted.'
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Pending follower does not exist anymore.',
                }
                return response_object, 404
        else:
            response_object = {
                'status': 'fail',
                'message': 'Request unauthorized.',
            }
            return response_object, 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'No pet found.'
        }
        return response_object, 404