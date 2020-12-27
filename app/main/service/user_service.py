import uuid
import datetime

from app.main import db
from app.main.model.user import User


def save_new_user(data, admin=False):
    user = User.query.filter_by(email=data['email']).first()
    user = user if user else User.query.filter_by(username=data['username']).first()
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


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()

def get_by_username(username):
    user = User.query.filter_by(username=username).first() 
    if user.admin is False:
        return user

def get_by_token(auth_token):
    decoded_resp = User.decode_auth_token(auth_token)
    if isinstance(decoded_resp, int):
        return User.query.filter_by(id=decoded_resp).first()
    return decoded_resp

def patch_a_user(public_id, auth_token, data):
    decoded_resp = User.decode_auth_token(auth_token)
    if isinstance(decoded_resp, int):
        user = User.query.filter_by(public_id=public_id).first() 

        if user and not User.query.filter_by(username=data["username"]).first() and not User.query.filter_by(email=data["email"]).first():
            if user.id == decoded_resp:
                user = User.query.filter_by(public_id=public_id).first()
        
                user.name = data["name"]
                user.username = data["username"]
                user.email = data["email"]
                user.password = data["password"]
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
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401