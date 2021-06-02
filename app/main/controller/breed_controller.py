from flask import request
from flask_restx import Resource

from ..util.dto import BreedDto
from ..util.decorator import *
from ..service.breed_service import save_new_breed, get_all_breeds, get_all_by_specie, get_a_breed, patch_a_breed, delete_a_breed

api = BreedDto.api
_breed = BreedDto.breed


@api.route('/')
class BreedList(Resource):
    @token_required
    @api.doc('list_of_registered_breeds')
    @api.marshal_list_with(_breed, envelope='data')
    def get(self, user_pid):
        """List all registered breeds"""
        return get_all_breeds()

    @admin_token_required
    @api.response(201, 'Breed successfully created.')
    @api.doc('create a new breed')
    @api.expect(_breed, validate=True)
    def post(self):
        """Creates a new Breed """
        data = request.json
        return save_new_breed(data=data)

@api.route('/parent/<parent_id>')
@api.param('parent_id', 'The Specie parent identifier')
class BreedListBySpecie(Resource):
    @token_required
    @api.doc('list_of_registered_breeds_by_specie_parent')
    @api.marshal_list_with(_breed, envelope='data')
    def get(self, user_pid, parent_id):
        """List all registered breeds"""
        breeds = get_all_by_specie(parent_id)
        if not isinstance(breeds, tuple):
            return breeds
        api.abort(breeds[1])

@api.route('/<public_id>')
@api.param('public_id', 'The Breed identifier')
@api.response(404, 'Breed not found.')
class Breed(Resource):
    @token_required
    @api.doc('get a breed')
    @api.marshal_with(_breed)
    def get(self, public_id):
        """get a breed given its identifier"""
        breed = get_a_breed(public_id)
        if not breed:
            api.abort(404)
        else:
            return breed

    @admin_token_required
    @api.response(201, 'Breed successfully updated.')
    @api.doc('patch a breed')
    @api.expect(_breed, validate=True)
    def patch(self, public_id):
        """patch a breed given its identifier"""
        return patch_a_breed(public_id, request.json)

    @admin_token_required
    @api.response(201, 'Breed successfully deleted.')
    @api.doc('delete a breed')
    @api.expect(_breed, validate=True)
    def delete(self, public_id):
        """delete a breed given its identifier"""
        return delete_a_breed(public_id, request.json)