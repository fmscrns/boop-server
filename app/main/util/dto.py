from flask_restx import Namespace, fields

class NullableString(fields.String):
    __schema_type__ = ['string', 'null']
    __schema_example__ = 'nullable string'

class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'name': fields.String(required=True, description='user name', min_length=2),
        'email': fields.String(required=True, description='user email address', pattern='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'),
        'username': fields.String(required=True, description='user username', min_length=2),
        'password': fields.String(required=True, description='user password', pattern='^(?!\s*$).+'),
        'public_id': fields.String(description='user Identifier'),
        "photo": fields.String(description="user profile photo"),
        "pet_count": fields.Integer(description="user pet count")
    })

class SpecieDto:
    api = Namespace('specie', description='specie related operations')
    specie = api.model('specie', {
        'name': fields.String(required=True, description='specie name', min_length=2),
        'public_id': fields.String(description='specie Identifier')
    })

class BreedDto:
    api = Namespace('breed', description='breed related operations')
    breed = api.model('breed', {
        'name': fields.String(required=True, description='breed name', min_length=2),
        'public_id': fields.String(description='breed Identifier'),
        'parent_name': fields.String(description='specie parent name'),
        'parent_id': fields.String(required=True, description='specie parent Identifier'),
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'username_or_email': fields.String(required=True, description='The username or email address', min_length=2),
        'password': fields.String(required=True, description='The user password '),
    })

class PetDto:
    api = Namespace("pet", description="pet related operations")
    
    pet = api.model("pet", {
        "public_id": fields.String(description="pet identifier"),
        "name": fields.String(required=True, description="pet name", min_length=2),
        "bio": fields.String(description="pet biography"),
        "birthday": fields.DateTime(dt_format="rfc822", description="pet birthday"),
        "sex": fields.Integer(required=True, description="pet sex", min=-1, max=1),
        "status": fields.Integer(required=True, description="pet status", min=-1, max=2),
        "is_private": fields.Integer(required=True, description="pet privacy", min=-1, max=1),
        "photo": fields.String(description="pet profile photo filename"),
        "registered_on": fields.DateTime(dt_format="rfc822", required=False, description="creation date"),
        "group_id": fields.String(required=True, description="specie identifier"),
        "group_name": fields.String(description="specie name"),
        "subgroup_id": fields.String(required=True, description="breed identifier"),
        "subgroup_name": fields.String(description="breed name"),
        "owner": fields.List(fields.Nested(
            api.model("owner", {
                "public_id": fields.String(description="user identifier", attribute="owner_id"),
                "name": fields.String(description="user name", attribute="owner_name"),
                "username": fields.String(description="user username", attribute="owner_username"),
                "photo": fields.String(description="user profile photo filename", attribute="owner_photo"),
            })
        ), description="pet owner"),
        "visitor_auth": fields.Integer(description="visiting user authorization"),
        
    })

class BusinessDto:
    api = Namespace("business", description="business related operations")
    
    business = api.model("business", {
        "public_id": fields.String(description="business identifier"),
        "name": fields.String(required=True, description="business name", min_length=2),
        "bio": fields.String(description="business biography"),
        "_type": fields.List(fields.Nested(
            api.model("_type", {
                "public_id": fields.String(required=True, description="type identifier", attribute="type_pid"),
                "name": fields.String(description="type name", attribute="type_name"),
            })
        ), required=True, description="business type"),
        "photo": fields.String(description="business profile photo filename"),
        "registered_on": fields.DateTime(dt_format="rfc822", required=False, description="creation date"),
        "executive": fields.List(fields.Nested(
            api.model("executive", {
                "public_id": fields.String(description="user identifier", attribute="executive_id"),
                "name": fields.String(description="user name", attribute="executive_name"),
                "username": fields.String(description="user username", attribute="executive_username"),
                "photo": fields.String(description="user profile photo filename", attribute="executive_photo"),
            })
        ), description="pet owner"),
        "visitor_auth": fields.Integer(description="visiting user authorization")
    })

class PostDto:
    api = Namespace("post", description="post related operations")
    
    post = api.model("post", {
        "public_id": fields.String(description="post identifier"),
        "content": fields.String(required=True, description="post content", min_length=1),
        "photo": fields.List(fields.Nested(
            api.model("photo", {
                "filename": NullableString(description="post photo filename", attribute="photo_filename"),
            })
        ), description="post photo"),
        "registered_on": fields.DateTime(dt_format="rfc822", required=False, description="creation date"),
        "creator_id": fields.String(description="user identifier"),
        "creator_name": fields.String(description="user name"),
        "creator_username": fields.String(description="user username"),
        "creator_photo": fields.String(description="user profile photo filename"),
        "pinboard_id": fields.String(description="business identifier"),
        "pinboard_name": fields.String(description="business name"),
        "pinboard_photo": fields.String(description="business photo"),
        "confiner_id": fields.String(description="circle identifier"),
        "confiner_name": fields.String(description="circle name"),
        "confiner_photo": fields.String(description="circle photo"),
        "subject": fields.List(fields.Nested(
            api.model("subject", {
                "public_id": fields.String(required=True, description="pet identifier", attribute="subject_id"),
                "name": fields.String(description="pet name", attribute="subject_name"),
                "photo": fields.String(description="pet profile photo filename", attribute="subject_photo"),
                "group_id": fields.String(description="specie  identifier"),
                "group_name": fields.String(description="specie name"),
                "subgroup_id": fields.String(description="breed identifier"),
                "subgroup_name": fields.String(description="breed name"),
                "visitor_auth": fields.Integer(description="visiting user authorization")
            })
        ), description="post subject", required=True),
        "is_mine": fields.Integer(description="visiting user ownership", min=0, max=1),
        "like_count": fields.Integer(description="post like count"),
        "comment_count": fields.Integer(description="post comment count"),
        "is_liked": fields.Integer(description="visiting user like", min=0, max=1)
        
    })

class CommentDto:
    api = Namespace("comment", description="comment related operations")
    
    comment = api.model("comment", {
        "public_id": fields.String(description="comment identifier"),
        "content": fields.String(required=True, description="comment content", min_length=1),
        "photo": fields.List(fields.Nested(
            api.model("photo", {
                "filename": NullableString(description="comment photo filename", attribute="photo_filename"),
            })
        ), description="comment photo"),
        "registered_on": fields.DateTime(dt_format="rfc822", required=False, description="creation date"),
        "creator_id": fields.String(description="user identifier"),
        "creator_name": fields.String(description="user name"),
        "creator_username": fields.String(description="user username"),
        "creator_photo": fields.String(description="user profile photo filename"),
        "parent_id": fields.String(description="post identifier"),
        "parent_name": fields.String(description="post name"),
        "parent_photo": fields.String(description="post photo")
    })

class BusinessTypeDto:
    api = Namespace('business_type', description='business type related operations')
    business_type = api.model('business_type', {
        'name': fields.String(required=True, description='business type name', min_length=2),
        'public_id': fields.String(description='business type Identifier')
    })


class CircleDto:
    api = Namespace("circle", description="circle related operations")
    
    circle = api.model("circle", {
        "public_id": fields.String(description="circle identifier"),
        "name": fields.String(required=True, description="circle name", min_length=2),
        "bio": fields.String(description="circle biography"),
        "_type": fields.List(fields.Nested(
            api.model("_type", {
                "public_id": fields.String(required=True, description="type identifier", attribute="type_pid"),
                "name": fields.String(description="type name", attribute="type_name"),
            })
        ), required=True, description="circle type"),
        "photo": fields.String(description="circle profile photo filename"),
        "registered_on": fields.DateTime(dt_format="rfc822", required=False, description="creation date"),
        "admin": fields.List(fields.Nested(
            api.model("admin", {
                "public_id": fields.String(description="user identifier", attribute="admin_id"),
                "name": fields.String(description="user name", attribute="admin_name"),
                "username": fields.String(description="user username", attribute="admin_username"),
                "photo": fields.String(description="user profile photo filename", attribute="admin_photo"),
            })
        ), description="circle admin"),
        "visitor_auth": fields.Integer(description="visiting user authorization"),
    })


class CircleTypeDto:
    api = Namespace('circle_type', description='circle type related operations')
    circle_type = api.model('circle_type', {
        'name': fields.String(required=True, description='circle type name', min_length=2),
        'public_id': fields.String(description='circle type Identifier')
    })

class NotificationDto:
    api = Namespace("notification", description="notification related operations")
    notification = api.model("notification", {
        "public_id": fields.String(description='notification identifier'),
        "content": fields.String(description="notification content", min_length=1),
        "_type": fields.Integer(description="notification type", min=-1, max=1),
        "is_read": fields.Boolean(description="notification read"),
        "registered_on": fields.DateTime(dt_format="rfc822", required=False, description="creation date"),
        "sender_photo": fields.String(description="notification photo filename"),
        "recipient_id": fields.String(description="user recipient identifier"),
        "pet_subject_id": fields.String(description="pet identifier"),
        "post_subject_id": fields.String(description="post identifier"),
        "circle_subject_id": fields.String(description="circle identifier"),
        "business_subject_id": fields.String(description="business identifier"),
        "notif_unread_count": fields.String(description="notification unread count")
    })