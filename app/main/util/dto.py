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

class PetDto:
    api = Namespace("pet", description="pet related operations")
    
    pet = api.model("pet", {
        "id": fields.String(description="pet identifier"),
        "name": fields.String(required=True, description="pet name"),
        "bio": fields.String(description="pet biography"),
        "birthday": fields.DateTime(dt_format="rfc822", description="pet birthday"),
        "sex": fields.Integer(required=True, description="pet sex"),
        "status": fields.Integer(required=True, description="pet status"),
        "photo": fields.String(description="pet profile photo filename"),
        "registered_on": fields.DateTime(description="creation date"),
        "owner_id": fields.String(description="user identifier"),
        "owner_name": fields.String(description="user name"),
        "owner_username": fields.String(description="user username"),
        "owner_photo": fields.String(description="user profile photo filename"),
        "group_id": fields.String(required=True, description="specie identifier"),
        "group_name": fields.String(description="specie name"),
        "subgroup_id": fields.String(required=True, description="breed identifier"),
        "subgroup_name": fields.String(description="breed name")
    })

class BusinessDto:
    api = Namespace("business", description="business related operations")
    
    business = api.model("business", {
        "id": fields.String(description="business identifier"),
        "name": fields.String(required=True, description="business name"),
        "bio": fields.String(description="business biography"),
        "_type": fields.Integer(required=True, description="business type", min=0, max=6),
        "photo": fields.String(description="business profile photo filename"),
        "registered_on": fields.DateTime(description="creation date"),
        "exec_id": fields.String(description="user identifier"),
        "exec_name": fields.String(description="user name"),
        "exec_username": fields.String(description="user username"),
        "exec_photo": fields.String(description="user profile photo filename")
    })