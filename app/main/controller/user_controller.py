from flask import request
from flask_restx import Resource
import time
from ..util.dto import UserDto
from ..util.decorator import *
from ..service.user_service import save_new_user, get_a_user, get_by_email, get_by_username, patch_a_user, get_by_token, get_all_by_search

api = UserDto.api
_user = UserDto.user
_userPatch = UserDto.user_patch


@api.route('/')
class UserList(Resource):
    @token_required
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self, user_pid):
        """List registered users"""
        time.sleep(1)
        return get_all_by_search(
            user_pid,
            request.args.get("search"),
            request.args.get("same_followed_pets", type=int),
            request.args.get("same_breed_preferences", type=int),
            request.args.get("pagination_no", type=int)
        )

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)

@api.route('/admin')
class AdminList(Resource):
    @api.doc('create a new admin user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new Admin """
        data = request.json
        return save_new_user(data=data, admin=True)

@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @token_required
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user

    @token_required
    @api.response(201, 'User successfully updated.')
    @api.doc('patch a user')
    @api.expect(_userPatch, validate=True)
    def patch(self, user_pid, public_id):
        """patch a user given its identifier"""
        return patch_a_user(user_pid, public_id, request.json)

    @token_required
    @api.response(201, 'User successfully updated.')
    @api.doc('patch a user')
    @api.expect(_userPatch, validate=True)
    def post(self, user_pid, public_id):
        """patch a user given its identifier"""
        return patch_a_user(user_pid, public_id, request.json, change_credentials=True)

@api.route('/email/<email>')
@api.param('email', 'The User identifier')
@api.response(404, 'User not found.')
class UserByEmail(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, email):
        """get a user given its email"""
        user = get_by_email(email)
        if not user:
            api.abort(404)
        else:
            return user

@api.route('/username/<username>')
@api.param('username', 'The User identifier')
@api.response(404, 'User not found.')
class UserByUsername(Resource):
    @token_required
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, user_pid, username):
        """get a user given its username"""
        user = get_by_username(username)
        if not user:
            api.abort(404)
        else:
            return user

@api.route('/bytoken')
@api.response(404, 'User not found.')
class UserByToken(Resource):
    @api.doc('get current user')
    @api.marshal_with(_user)
    def get(self):
        """get current user given its token"""
        auth_header = request.headers.get('Authorization')
        get_resp = get_by_token(auth_header.split(" ")[1])
        if isinstance(get_resp, str):
            api.abort(401, message=get_resp)
        else:
            return get_resp