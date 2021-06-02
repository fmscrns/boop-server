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
        "public_id": fields.String(description="pet identifier"),
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
        "public_id": fields.String(description="business identifier"),
        "name": fields.String(required=True, description="business name"),
        "bio": fields.String(description="business biography"),
        "_type": fields.List(fields.Nested(
            api.model("_type", {
                "public_id": fields.String(required=True, description="type identifier", attribute="type_pid"),
                "name": fields.String(description="type name", attribute="type_name"),
            })
        ), required=True, description="business type"),
        "photo": fields.String(description="business profile photo filename"),
        "registered_on": fields.DateTime(description="creation date"),
        "executive_id": fields.String(description="user identifier"),
        "executive_name": fields.String(description="user name"),
        "executive_username": fields.String(description="user username"),
        "executive_photo": fields.String(description="user profile photo filename")
    })

class PostDto:
    api = Namespace("post", description="post related operations")
    
    post = api.model("post", {
        "public_id": fields.String(description="post identifier"),
        "content": fields.String(required=True, description="post content"),
        "photo": fields.String(description="post photo"),
        "registered_on": fields.DateTime(description="creation date"),
        "creator_id": fields.String(description="user identifier"),
        "creator_name": fields.String(description="user name"),
        "creator_username": fields.String(description="user username"),
        "creator_photo": fields.String(description="user profile photo filename"),
        "pinboard_id": fields.String(description="business identifier"),
        "confiner_id": fields.String(description="circle identifier")
    })

class BusinessTypeDto:
    api = Namespace('business_type', description='business type related operations')
    business_type = api.model('business_type', {
        'name': fields.String(required=True, description='business type name'),
        'public_id': fields.String(description='business type Identifier')
    })


class CircleDto:
    api = Namespace("circle", description="circle related operations")
    
    circle = api.model("circle", {
        "public_id": fields.String(description="circle identifier"),
        "name": fields.String(required=True, description="circle name"),
        "bio": fields.String(description="circle biography"),
        "_type": fields.List(fields.Nested(
            api.model("_type", {
                "public_id": fields.String(required=True, description="type identifier", attribute="type_pid"),
                "name": fields.String(description="type name", attribute="type_name"),
            })
        ), required=True, description="circle type"),
        "photo": fields.String(description="circle profile photo filename"),
        "registered_on": fields.DateTime(description="creation date"),
        "admin_id": fields.String(description="user identifier"),
        "admin_name": fields.String(description="user name"),
        "admin_username": fields.String(description="user username"),
        "admin_photo": fields.String(description="user profile photo filename"),
        "visitor_auth": fields.Integer(description="visiting user authorization"),
        "member_count": fields.Integer(description="member count")
    })


class CircleTypeDto:
    api = Namespace('circle_type', description='circle type related operations')
    circle_type = api.model('circle_type', {
        'name': fields.String(required=True, description='circle type name'),
        'public_id': fields.String(description='circle type Identifier')
    })