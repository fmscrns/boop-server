from flask import request
from flask_restx import Resource

from ..util.dto import SpecieDto
from ..util.decorator import *
from ..service.specie_service import save_new_specie, get_all_species, get_a_specie

api = SpecieDto.api
_specie = SpecieDto.specie


@api.route('/')
class SpecieList(Resource):
    @token_required
    @api.doc('list_of_registered_species')
    @api.marshal_list_with(_specie, envelope='data')
    def get(self):
        """List all registered species"""
        return get_all_species()

    @admin_token_required
    @api.response(201, 'Specie successfully created.')
    @api.doc('create a new specie')
    @api.expect(_specie, validate=True)
    def post(self):
        """Creates a new Specie """
        data = request.json
        return save_new_specie(data=data)

@api.route('/<public_id>')
@api.param('public_id', 'The Specie identifier')
@api.response(404, 'Specie not found.')
class Specie(Resource):
    @token_required
    @api.doc('get a specie')
    @api.marshal_with(_specie)
    def get(self, public_id):
        """get a specie given its identifier"""
        specie = get_a_specie(public_id)
        if not specie:
            api.abort(404)
        else:
            return specie

    @api.response(201, 'Specie successfully updated.')
    @api.doc('patch a specie')
    @api.expect(_specie, validate=True)
    def patch(self, public_id):
        """patch a specie given its identifier"""
        return patch_a_specie(public_id, request.json)

    
    @api.response(201, 'Specie successfully deleted.')
    @api.doc('delete a specie')
    @api.expect(_specie, validate=True)
    def patch(self, public_id):
        """delete a specie given its identifier"""
        return delete_a_specie(public_id, request.json)