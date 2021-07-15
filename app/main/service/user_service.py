from app.main.model.preference import Preference
from sqlalchemy.sql.expression import outerjoin
from app.main.model.pet import Pet
import uuid
import datetime
from flask.globals import current_app
from sqlalchemy import or_, func
from app.main import db
from app.main.model.user import User, pet_follower_table

def save_new_user(data, admin=False):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        user = User.query.filter_by(username=data['username']).first()
    
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            name=data["name"],
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        if admin is True:
            new_user.admin = True
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please sign in instead.',
        }
        return response_object, 409

def get_all_by_search(requestor_pid, value, same_fp, same_bpref, pagination_no):
    return [
        dict(
            public_id = user[0],
            name = user[1],
            username = user[2],
            photo = user[3]
        ) for user in db.session.query(
            User.public_id,
            User.name,
            User.username,
            User.photo,
            func.count(pet_follower_table.c.pet_pid)
        ).select_from(
            User
        ).filter(
            or_(User.name.ilike("%{}%".format(value)),
            User.username.ilike("%{}%".format(value)))
        ).filter(
            User.public_id != requestor_pid
        ).filter(
            User.admin != True
        ).outerjoin(
            pet_follower_table
        ).outerjoin(
            Pet
        ).filter(
            (Pet.public_id.in_(
                db.session.query(
                    pet_follower_table.c.pet_pid
                ).select_from(
                    pet_follower_table
                ).filter(
                    pet_follower_table.c.follower_pid == requestor_pid
                ).subquery()
            )) if same_fp == 1 else (User.public_id == User.public_id)
        ).outerjoin(
            Preference
        ).filter(
            (Preference.breed_subgroup_id.in_(
                db.session.query(
                    Preference.breed_subgroup_id
                ).select_from(
                    Preference
                ).filter(
                    Preference.user_selector_id == requestor_pid
                ).subquery()
            )) if same_bpref == 1 else (User.public_id == User.public_id)
        ).group_by(
            User.public_id,
            User.name,
            User.username,
            User.photo
        ).paginate(
            page=pagination_no,
            per_page= current_app.config["PER_PAGE_PAGINATION"]
        ).items
    ]

def get_a_user(public_id):
    user = db.session.query(
        User.public_id,
        User.name,
        User.username,
        User.photo
    ).filter(
        User.public_id == public_id
    ).filter(
        User.admin != True
    ).first()
    if user:
        return dict(
            public_id = user[0],
            name = user[1],
            username = user[2],
            photo = user[3],
            pet_count = db.session.query(
                func.count(pet_follower_table.c.public_id)
            ).filter(
                pet_follower_table.c.follower_pid == public_id
            ).filter(
                pet_follower_table.c.is_owner == True
            ).scalar()
        )

def get_by_email(email):
    return User.query.filter_by(email=email).first() 

def get_by_username(username):
    user = db.session.query(
        User.public_id,
        User.name,
        User.username,
        User.photo
    ).filter(
        User.username == username
    ).filter(
        User.admin != True
    ).first()
    if user:
        return dict(
            public_id = user[0],
            name = user[1],
            username = user[2],
            photo = user[3],
            pet_count = db.session.query(
                func.count(pet_follower_table.c.public_id)
            ).filter(
                pet_follower_table.c.follower_pid == user[0]
            ).filter(
                pet_follower_table.c.is_owner == True
            ).scalar()
        )

def get_by_token(auth_token):
    decoded_resp = User.decode_auth_token(auth_token)
    if isinstance(decoded_resp, int):
        user = db.session.query(
            User.public_id,
            User.name,
            User.username,
            User.photo,
            User.email
        ).filter(
            User.id == decoded_resp
        ).first()
        if user:
            return dict(
                public_id = user[0],
                name = user[1],
                username = user[2],
                photo = user[3],
                email = user[4],
                pet_count = db.session.query(
                    func.count(pet_follower_table.c.public_id)
                ).filter(
                    pet_follower_table.c.follower_pid == user[0]
                ).filter(
                    pet_follower_table.c.is_owner == True
                ).scalar()
            )
    return decoded_resp

def patch_a_user(requestor_pid, public_id, data, change_credentials=False):
    if requestor_pid == public_id:
        requesting_user = User.query.filter_by(public_id=public_id).first() 

        if change_credentials is False:
            requesting_user.name = data["name"] if data.get("name") else requesting_user.name
            requesting_user.photo = data["photo"] if data.get("photo") else requesting_user.photo
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Successfully updated.'
            }
            return response_object, 201
        elif change_credentials is True:
            if data.get("username"):
                user_by_username = User.query.filter_by(username=data["username"]).first()
                if not user_by_username or user_by_username == requesting_user:
                    requesting_user.username = data["username"]
                    db.session.commit()
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully updated.'
                    }
                    return response_object, 201
                else:
                    response_object = {
                    'status': 'fail',
                    'message': 'Username is already used.'
                }
                return response_object, 409

            elif data.get("email"):
                user_by_email = User.query.filter_by(email=data["email"]).first()
                if not user_by_email or user_by_email == requesting_user:
                    requesting_user.email = data["email"]
                    db.session.commit()
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully updated.'
                    }
                    return response_object, 201
                else:
                    response_object = {
                    'status': 'fail',
                    'message': 'Email is already used.'
                }
                return response_object, 409

            elif data.get("password"):
                requesting_user.password = data["password"]
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'message': 'Successfully updated.'
                }
                return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'User does not exist.',
            }
            return response_object, 404
    else:
        response_object = {
            'status': 'fail',
            'message': 'Forbidden.',
        }
        return response_object, 403

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401