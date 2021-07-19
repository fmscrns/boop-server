from flask import request
from flask_restx import Resource
from ..util.dto import BusinessDto, UserDto
from ..util.decorator import *
from ..service.business_service import get_all_businesses_by_preference, save_new_business, get_all_businesses, get_all_businesses_by_user, get_a_business, patch_a_business, delete_a_business
from ..service.businessFollower_service import create_business_follower, get_all_business_followers, delete_business_follower, create_business_executive, delete_business_executive

api = BusinessDto.api
_business = BusinessDto.business
_user = UserDto.user

@api.route('/')
class BusinessList(Resource):
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
        return get_all_businesses_by_user(user_pid, exec_id)

@api.route('/preference')
class BusinessListByPreference(Resource):
    @token_required
    @api.doc('list_of_registered_businesses')
    @api.marshal_list_with(_business, envelope='data')
    def get(self, user_pid):
        """List all registered businesses"""
        return get_all_businesses_by_preference(user_pid, request.args.get("pagination_no", type=int))

@api.route('/<public_id>')
@api.param('public_id', 'The Business identifier')
@api.response(404, 'Business not found.')
class Business(Resource):
    @token_required
    @api.doc('get a business')
    @api.marshal_with(_business)
    def get(self, user_pid, public_id):
        """get a business given its identifier"""
        business = get_a_business(user_pid, public_id)
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
        return patch_a_business(public_id, user_pid, request.json)

    @token_required
    @api.response(201, 'Business successfully deleted.')
    @api.doc('delete a business')
    @api.expect(_business, validate=True)
    def delete(self, user_pid, public_id):
        """delete a business given its identifier"""
        return delete_a_business(public_id, user_pid, request.json)

@api.route('/<public_id>/follower/')
@api.param('public_id', 'The Business identifier')
@api.response(404, 'Business not found.')
class BusinessFollowerList(Resource):    
    @token_required
    @api.doc('list_of_registered_business_followers')
    @api.marshal_list_with(_user, envelope='data')
    def get(self, user_pid, public_id):
        """List all registered business followers"""
        return get_all_business_followers(user_pid, public_id)

    @token_required
    @api.doc('create business follower')
    def post(self, user_pid, public_id):
        """create business follower given business identifier"""
        return create_business_follower(user_pid, public_id)

@api.route('/<public_id>/follower/<follower_id>')
@api.param('public_id', 'The Business identifier')
@api.param('follower_id', 'The User identifier')
@api.response(404, 'Business not found.')
class BusinessFollower(Resource):
    @token_required
    @api.response(201, 'Business follower successfully deleted.')
    @api.doc('delete business follower')
    def delete(self, user_pid, public_id, follower_id):
        """delete business follower given business identifier"""
        return delete_business_follower(user_pid, public_id, follower_id)

@api.route('/<public_id>/executive/')
@api.param('public_id', 'The Business identifier')
@api.response(404, 'Business not found.')
class BusinessExecutiveList(Resource):
    @token_required
    @api.response(201, 'Business successfully have new executive.')
    @api.doc('create business executive')
    def post(self, user_pid, public_id):
        """create business executive given business identifier"""
        return create_business_executive(user_pid, public_id, request.json)

@api.route('/<public_id>/executive/<executive_id>')
@api.param('public_id', 'The Business identifier')
@api.param('executive_id', 'The User identifier')
@api.response(404, 'Business not found.')
class BusinessExecutive(Resource):
    @token_required
    @api.response(201, 'Business executive successfully removed.')
    @api.doc('remove business executive given business identifier')
    def delete(self, user_pid, public_id, executive_id):
        """delete a business given its identifier"""
        return delete_business_executive(user_pid, public_id, executive_id, request.json)