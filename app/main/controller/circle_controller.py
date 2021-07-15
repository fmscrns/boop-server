import time
from flask import request
from flask_restx import Resource

from ..util.dto import CircleDto, UserDto
from ..util.decorator import *
from ..service.circle_service import save_new_circle, get_all_circles_by_user, get_a_circle, patch_a_circle, delete_a_circle, get_all_circles_by_preference
from ..service.circleMember_service import create_circle_member, delete_circle_member, get_all_circle_members, accept_circle_member, create_circle_admin, delete_circle_admin

api = CircleDto.api
_circle = CircleDto.circle
_user = UserDto.user

@api.route('/')
class CircleList(Resource):
    @token_required
    @api.response(201, 'Circle successfully created.')
    @api.doc('create a new circle')
    @api.expect(_circle, validate=True)
    def post(self, user_pid):
        """Creates a new Circle """
        data = request.json
        save_circle_resp = save_new_circle(user_pid=user_pid, data=data)

        if isinstance(save_circle_resp, tuple):
            return save_circle_resp
        else:
            api.abort(save_circle_resp)

@api.route('/creator/<creator_id>')
@api.param("creator_id", "The User public identifier")
class CircleListByUser(Resource):
    @token_required
    @api.doc('list_of_registered_circles')
    @api.marshal_list_with(_circle, envelope='data')
    def get(self, user_pid, creator_id):
        """List all registered circles"""
        return get_all_circles_by_user(user_pid, creator_id)

@api.route('/preference')
class CircleListByPreference(Resource):
    @token_required
    @api.doc('list_of_registered_circles')
    @api.marshal_list_with(_circle, envelope='data')
    def get(self, user_pid):
        """List all registered circles"""
        time.sleep(1)
        return get_all_circles_by_preference(user_pid, request.args.get("pagination_no", type=int))

@api.route('/<public_id>')
@api.param('public_id', 'The Circle identifier')
@api.response(404, 'Circle not found.')
class Circle(Resource):
    @token_required
    @api.doc('get a circle')
    @api.marshal_with(_circle)
    def get(self, user_pid, public_id):
        """get a circle given its identifier"""
        circle = get_a_circle(user_pid, public_id)
        if not circle:
            api.abort(404)
        else:
            return circle
        
    @token_required
    @api.response(201, 'Circle successfully updated.')
    @api.doc('patch a circle')
    @api.expect(_circle, validate=True)
    def patch(self, user_pid, public_id):
        """patch a circle given its identifier"""
        return patch_a_circle(public_id, user_pid, request.json)

    @token_required
    @api.response(201, 'Circle successfully deleted.')
    @api.doc('delete a circle')
    @api.expect(_circle, validate=True)
    def delete(self, user_pid, public_id):
        """delete a circle given its identifier"""
        return delete_a_circle(public_id, user_pid, request.json)

@api.route('/<public_id>/member/')
@api.param('public_id', 'The Circle identifier')
@api.response(404, 'Circle not found.')
class CircleMemberList(Resource):    
    @token_required
    @api.doc('list_of_registered_circle_members')
    @api.marshal_list_with(_user, envelope='data')
    def get(self, user_pid, public_id):
        """List all registered circle members"""
        return get_all_circle_members(user_pid, public_id, request.args.get("type"), request.args.get("search"))

    @token_required
    @api.doc('create circle member')
    def post(self, user_pid, public_id):
        """create circle member given circle identifier"""
        return create_circle_member(user_pid, public_id)

@api.route('/<public_id>/member/<member_id>')
@api.param('public_id', 'The Circle identifier')
@api.param('member_id', 'The User identifier')
@api.response(404, 'Circle not found.')
class CircleMember(Resource):   
    @token_required
    @api.response(201, 'Circle member successfully accepted.')
    @api.doc('accept circle member')
    def post(self, user_pid, public_id, member_id):
        """accept circle member given circle identifier"""
        return accept_circle_member(user_pid, public_id, member_id)

    @token_required
    @api.response(201, 'Circle member successfully deleted.')
    @api.doc('delete circle member')
    def delete(self, user_pid, public_id, member_id):
        """delete circle member given circle identifier"""
        return delete_circle_member(user_pid, public_id, member_id)

@api.route('/<public_id>/admin/')
@api.param('public_id', 'The Circle identifier')
@api.response(404, 'Circle not found.')
class CircleAdminList(Resource):
    @token_required
    @api.response(201, 'Circle successfully have new admin.')
    @api.doc('create circle admin')
    def post(self, user_pid, public_id):
        """create circle admin given circle identifier"""
        return create_circle_admin(user_pid, public_id, request.json)

@api.route('/<public_id>/admin/<admin_id>')
@api.param('public_id', 'The Circle identifier')
@api.param('admin_id', 'The User identifier')
@api.response(404, 'Circle not found.')
class CircleAdmin(Resource):
    @token_required
    @api.response(201, 'Circle admin successfully removed.')
    @api.doc('remove circle admin given circle identifier')
    def delete(self, user_pid, public_id, admin_id):
        """delete a circle given its identifier"""
        return delete_circle_admin(user_pid, public_id, admin_id, request.json)