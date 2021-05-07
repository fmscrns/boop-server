from flask import request
from flask_restx import Resource

from ..util.dto import CircleDto
from ..util.decorator import *
from ..service.circle_service import save_new_circle, get_all_circles_by_user, get_a_circle, patch_a_circle, delete_a_circle

api = CircleDto.api
_circle = CircleDto.circle


@api.route('/')
class CircleList(Resource):
    # @admin_token_required
    # @api.doc('list_of_registered_circles')
    # @api.marshal_list_with(_circle, envelope='data')
    # def get(self):
    #     """List all registered circles"""
    #     return get_all_circles()

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

@api.route('/admin/<admin_id>')
@api.param("admin_id", "The User public identifier")
class CircleListByUser(Resource):
    @token_required
    @api.doc('list_of_registered_circles')
    @api.marshal_list_with(_circle, envelope='data')
    def get(self, user_pid, admin_id):
        """List all registered circles"""
        return get_all_circles_by_user(admin_id)

@api.route('/<public_id>')
@api.param('public_id', 'The Circle identifier')
@api.response(404, 'Circle not found.')
class Circle(Resource):
    @token_required
    @api.doc('get a circle')
    @api.marshal_with(_circle)
    def get(self, user_pid, public_id):
        """get a circle given its identifier"""
        circle = get_a_circle(public_id)
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
        print("HELLO")
        return patch_a_circle(public_id, user_pid, request.json)

    @token_required
    @api.response(201, 'Circle successfully deleted.')
    @api.doc('delete a circle')
    @api.expect(_circle, validate=True)
    def delete(self, user_pid, public_id):
        """delete a circle given its identifier"""
        return delete_a_circle(public_id, user_pid, request.json)