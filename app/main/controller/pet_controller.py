from flask import request
from flask_restx import Resource

from ..util.dto import PetDto
from ..util.decorator import *
from ..service.pet_service import save_new_pet, get_all_pets_by_user, get_a_pet, patch_a_pet, delete_a_pet

api = PetDto.api
_pet = PetDto.pet


@api.route('/')
class PetList(Resource):
    # @admin_token_required
    # @api.doc('list_of_registered_pets')
    # @api.marshal_list_with(_pet, envelope='data')
    # def get(self):
    #     """List all registered pets"""
    #     return get_all_pets()

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
        return get_all_pets_by_user(owner_id)

@api.route('/<public_id>')
@api.param('public_id', 'The Pet identifier')
@api.response(404, 'Pet not found.')
class Pet(Resource):
    @token_required
    @api.doc('get a pet')
    @api.marshal_with(_pet)
    def get(self, user_pid, public_id):
        """get a pet given its identifier"""
        pet = get_a_pet(public_id)
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