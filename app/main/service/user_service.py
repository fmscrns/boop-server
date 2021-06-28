from app.main.model.notification import Notification
import uuid
import datetime
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

def get_all_users():
    return User.query.all()

def get_all_by_search(value):
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
            User.photo
        ).filter(
            or_(User.name.ilike("%{}%".format(value)),
            User.username.ilike("%{}%".format(value)))
        ).filter(
            User.admin != True
        ).all()
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
            User.photo
        ).filter(
            User.id == decoded_resp
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
    return decoded_resp

def patch_a_user(public_id, auth_token, data):
    decoded_resp = User.decode_auth_token(auth_token)
    if isinstance(decoded_resp, int):
        user = User.query.filter_by(public_id=public_id).first() 

        user_by_username = User.query.filter_by(username=data["username"]).first()
        user_by_email = User.query.filter_by(email=data["email"]).first()

        if user and (not user_by_username or user_by_username == user) and (not user_by_email or user_by_email == user):
            if user.id == decoded_resp:
                user.name = data["name"]
                user.username = data["username"]
                user.email = data["email"]
                user.password = data["password"]
                user.photo = data["photo"]
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'message': 'Successfully updated.',
                    'payload': user.username
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Forbidden to update.',
                }
                return response_object, 403
        else:
            response_object = {
                'status': 'fail',
                'message': 'User does not exist or username and email has been used already.',
            }
            return response_object, 404
    return decoded_resp

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