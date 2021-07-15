from flask import request
from flask_restx import Resource

from ..util.dto import BusinessTypeDto
from ..util.decorator import *
from ..service.businessType_service import save_new_businessType, get_all_businessTypes, get_a_businessType, patch_a_businessType, delete_a_businessType

api = BusinessTypeDto.api
_businessType = BusinessTypeDto.business_type

@api.route('/')
class BusinessTypeList(Resource):
    @token_required
    @api.doc('list_of_registered_business_types')
    @api.marshal_list_with(_businessType, envelope='data')
    def get(self, user_pid):
        """List all registered business types"""
        return get_all_businessTypes(user_pid)

    @admin_token_required
    @api.response(201, 'Business type successfully created.')
    @api.doc('create a new business type')
    @api.expect(_businessType, validate=True)
    def post(self):
        """Creates a new Business type """
        data = request.json
        return save_new_businessType(data=data)

@api.route('/<public_id>')
@api.param('public_id', 'The Business type identifier')
@api.response(404, 'Business type not found.')
class BusinessType(Resource):
    @token_required
    @api.doc('get a business type')
    @api.marshal_with(_businessType)
    def get(self, public_id):
        """get a business type given its identifier"""
        business_type = get_a_businessType(public_id)
        if not business_type:
            api.abort(404)
        else:
            return business_type

    @admin_token_required
    @api.response(201, 'Business type successfully updated.')
    @api.doc('patch a business type')
    @api.expect(_businessType, validate=True)
    def patch(self, public_id):
        """patch a business type given its identifier"""
        return patch_a_businessType(public_id, request.json)

    @admin_token_required
    @api.response(201, 'Business type successfully deleted.')
    @api.doc('delete a business type')
    @api.expect(_businessType, validate=True)
    def delete(self, public_id):
        """delete a business type given its identifier"""
        return delete_a_businessType(public_id, request.json)