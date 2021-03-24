from flask import request
from flask_restx import Resource

from ..util.dto import BusinessDto
from ..util.decorator import *
from ..service.business_service import save_new_business, get_all_businesses_by_user, get_a_business, patch_a_business, delete_a_business

api = BusinessDto.api
_business = BusinessDto.business


@api.route('/')
class BusinessList(Resource):
    # @admin_token_required
    # @api.doc('list_of_registered_businesses')
    # @api.marshal_list_with(_business, envelope='data')
    # def get(self):
    #     """List all registered businesses"""
    #     return get_all_businesses()

    @token_required
    @api.response(201, 'Business successfully created.')
    @api.doc('create a new business')
    @api.expect(_business, validate=True)
    def post(self, user_pid):
        """Creates a new Business """
        data = request.json
        save_business_resp = save_new_business(user_pid=user_pid, data=data)

        if isinstance(save_business_resp, tuple):
            return save_business_resp
        else:
            api.abort(save_business_resp)

@api.route('/exec/<exec_id>')
@api.param("exec_id", "The User public identifier")
class BusinessListByUser(Resource):
    @token_required
    @api.doc('list_of_registered_businesses')
    @api.marshal_list_with(_business, envelope='data')
    def get(self, user_pid, exec_id):
        """List all registered businesses"""
        return get_all_businesses_by_user(exec_id)

@api.route('/<public_id>')
@api.param('public_id', 'The Business identifier')
@api.response(404, 'Business not found.')
class Business(Resource):
    @token_required
    @api.doc('get a business')
    @api.marshal_with(_business)
    def get(self, user_pid, public_id):
        """get a business given its identifier"""
        business = get_a_business(public_id)
        if not business:
            api.abort(404)
        else:
            return business

    @token_required
    @api.response(201, 'Business successfully updated.')
    @api.doc('patch a business')
    @api.expect(_business, validate=True)
    def patch(self, user_pid, public_id):
        """patch a business given its identifier"""
        print("HELLO")
        return patch_a_business(public_id, user_pid, request.json)

    @token_required
    @api.response(201, 'Business successfully deleted.')
    @api.doc('delete a business')
    @api.expect(_business, validate=True)
    def delete(self, user_pid, public_id):
        """delete a business given its identifier"""
        return delete_a_business(public_id, user_pid, request.json)