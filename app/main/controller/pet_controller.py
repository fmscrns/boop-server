from flask import request
from flask_restx import Resource

from ..util.dto import PetDto, UserDto
from ..util.decorator import *
from ..service.pet_service import save_new_pet, get_all_pets_by_user, get_a_pet, patch_a_pet, delete_a_pet, get_all_pets_by_preference, get_all_by_search
from ..service.petFollower_service import create_pet_owner, get_all_pet_followers, create_pet_follower, delete_pet_follower, accept_pet_follower, delete_pet_owner

api = PetDto.api
_pet = PetDto.pet
_user = UserDto.user

@api.route('/')
class PetList(Resource):
    @token_required
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_pet, envelope='data')
    def get(self, user_pid):
        """List registered users"""
        return get_all_by_search(
            request.args.get("search"),
            request.args.get("group_id"),
            request.args.get("subgroup_id"),
            request.args.get("status"),
            request.args.get("pagination_no",
            type=int)
        )

    @token_required
    @api.response(201, 'Pet successfully created.')
    @api.doc('create a new pet')
    @api.expect(_pet, validate=True)
    def post(self, user_pid):
        """Creates a new Pet """
        data = request.json
        return save_new_pet(user_pid=user_pid, data=data)

@api.route('/owner/<owner_id>')
@api.param("owner_id", "The User public identifier")
class PetListByUser(Resource):
    @token_required
    @api.doc('list_of_registered_pets')
    @api.marshal_list_with(_pet, envelope='data')
    def get(self, user_pid, owner_id):
        """List all registered pets"""
        return get_all_pets_by_user(user_pid, owner_id, request.args.get("tag_suggestions"))

@api.route('/preference')
class PetListByPreference(Resource):
    @token_required
    @api.doc('list_of_registered_pets')
    @api.marshal_list_with(_pet, envelope='data')
    def get(self, user_pid):
        """List all registered pets"""
        return get_all_pets_by_preference(user_pid, request.args.get("pagination_no", type=int))

@api.route('/<public_id>')
@api.param('public_id', 'The Pet identifier')
@api.response(404, 'Pet not found.')
class Pet(Resource):
    @token_required
    @api.doc('get a pet')
    @api.marshal_with(_pet)
    def get(self, user_pid, public_id):
        """get a pet given its identifier"""
        pet = get_a_pet(user_pid, public_id)
        if not pet:
            api.abort(404)
        else:
            return pet

    @token_required
    @api.response(201, 'Pet successfully updated.')
    @api.doc('patch a pet')
    @api.expect(_pet, validate=True)
    def patch(self, user_pid, public_id):
        """patch a pet given its identifier"""
        return patch_a_pet(public_id, user_pid, request.json)

    @token_required
    @api.response(201, 'Pet successfully deleted.')
    @api.doc('delete a pet')
    @api.expect(_pet, validate=True)
    def delete(self, user_pid, public_id):
        """delete a pet given its identifier"""
        return delete_a_pet(public_id, user_pid, request.json)

@api.route('/<public_id>/follower/')
@api.param('public_id', 'The Pet identifier')
@api.response(404, 'Pet not found.')
class PetFollowerList(Resource):
    @token_required
    @api.doc('list_of_registered_pet_followers')
    @api.marshal_list_with(_user, envelope='data')
    def get(self, user_pid, public_id):
        """List all registered pet followers"""
        return get_all_pet_followers(user_pid, public_id, request.args.get("type"))

    @token_required
    @api.response(201, 'Pet successfully followed.')
    @api.doc('create pet follower')
    def post(self, user_pid, public_id):
        """create pet follower given pet identifier"""
        return create_pet_follower(user_pid, public_id)

@api.route('/<public_id>/follower/<follower_id>')
@api.param('public_id', 'The Pet identifier')
@api.param('follower_id', 'The User identifier')
@api.response(404, 'Circle not found.')
class PetFollower(Resource):
    @token_required
    @api.response(201, 'Pet follower successfully accepted.')
    @api.doc('accept pet follower')
    def post(self, user_pid, public_id, follower_id):
        """accept pet follower given pet identifier"""
        return accept_pet_follower(user_pid, public_id, follower_id)

    @token_required
    @api.response(201, 'Pet successfully unfollowed.')
    @api.doc('delete pet follower given pet identifier')
    def delete(self, user_pid, public_id, follower_id):
        """delete a pet given its identifier"""
        return delete_pet_follower(user_pid, public_id, follower_id)

@api.route('/<public_id>/owner/')
@api.param('public_id', 'The Pet identifier')
@api.response(404, 'Pet not found.')
class PetOwnerList(Resource):
    @token_required
    @api.response(201, 'Pet successfully have new owner.')
    @api.doc('create pet owner')
    def post(self, user_pid, public_id):
        """create pet owner given pet identifier"""
        return create_pet_owner(user_pid, public_id, request.json)

@api.route('/<public_id>/owner/<owner_id>')
@api.param('public_id', 'The Pet identifier')
@api.param('owner_id', 'The User identifier')
@api.response(404, 'Circle not found.')
class PetOwner(Resource):
    @token_required
    @api.response(201, 'Pet owner successfully removed.')
    @api.doc('remove pet owner given pet identifier')
    def delete(self, user_pid, public_id, owner_id):
        """delete a pet given its identifier"""
        return delete_pet_owner(user_pid, public_id, owner_id, request.json)