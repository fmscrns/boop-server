from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'name': fields.String(required=True, description='user name'),
        'email': fields.String(required=True, description='user email address', pattern='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier'),
        "photo": fields.String(description="user profile photo"),
    })

class SpecieDto:
    api = Namespace('specie', description='specie related operations')
    specie = api.model('specie', {
        'name': fields.String(required=True, description='specie name'),
        'public_id': fields.String(description='specie Identifier')
    })

class BreedDto:
    api = Namespace('breed', description='breed related operations')
    breed = api.model('breed', {
        'name': fields.String(required=True, description='breed name'),
        'public_id': fields.String(description='breed Identifier'),
        'parent_name': fields.String(description='specie parent name'),
        'parent_id': fields.String(required=True, description='specie parent Identifier'),
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'username_or_email': fields.String(required=True, description='The username or email address'),
        'password': fields.String(required=True, description='The user password '),
    })