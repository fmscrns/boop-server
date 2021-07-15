from flask import request
from flask_restx import Resource

from ..util.dto import CircleTypeDto
from ..util.decorator import *
from ..service.circleType_service import save_new_circleType, get_all_circleTypes, get_a_circleType, patch_a_circleType, delete_a_circleType

api = CircleTypeDto.api
_circleType = CircleTypeDto.circle_type

@api.route('/')
class CircleTypeList(Resource):
    @token_required
    @api.doc('list_of_registered_circle_types')
    @api.marshal_list_with(_circleType, envelope='data')
    def get(self, user_pid):
        """List all registered circle types"""
        return get_all_circleTypes(user_pid)

    @admin_token_required
    @api.response(201, 'Circle type successfully created.')
    @api.doc('create a new circle type')
    @api.expect(_circleType, validate=True)
    def post(self):
        """Creates a new Circle type """
        data = request.json
        return save_new_circleType(data=data)

@api.route('/<public_id>')
@api.param('public_id', 'The Circle type identifier')
@api.response(404, 'Circle type not found.')
class CircleType(Resource):
    @token_required
    @api.doc('get a circle type')
    @api.marshal_with(_circleType)
    def get(self, public_id):
        """get a circle type given its identifier"""
        circle_type = get_a_circleType(public_id)
        if not circle_type:
            api.abort(404)
        else:
            return circle_type

    @admin_token_required
    @api.response(201, 'Circle type successfully updated.')
    @api.doc('patch a circle type')
    @api.expect(_circleType, validate=True)
    def patch(self, public_id):
        """patch a circle type given its identifier"""
        return patch_a_circleType(public_id, request.json)

    @admin_token_required
    @api.response(201, 'Circle type successfully deleted.')
    @api.doc('delete a circle type')
    @api.expect(_circleType, validate=True)
    def delete(self, public_id):
        """delete a circle type given its identifier"""
        return delete_a_circleType(public_id, request.json)