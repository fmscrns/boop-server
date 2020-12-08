from flask import request
from flask_restx import Resource

from ..util.dto import UserDto
from ..util.decorator import *
from ..service.user_service import save_new_user, get_all_users, get_a_user, get_by_username, patch_a_user, get_by_token

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @admin_token_required
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

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

    @api.response(201, 'User successfully updated.')
    @api.doc('patch a user')
    @api.expect(_user, validate=True)
    def patch(self, public_id):
        """patch a user given its identifier"""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            patch_user = patch_a_user(public_id, auth_header.split(" ")[1], request.json)

            if isinstance(patch_user, str):
                api.abort(401, message=patch_user)
            else:
                return patch_user

@api.route('/username/<username>')
@api.param('username', 'The User identifier')
@api.response(404, 'User not found.')
class UserByUsername(Resource):
    @token_required
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, username):
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