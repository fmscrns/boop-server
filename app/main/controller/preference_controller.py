from flask import request
from flask_restx import Resource
from ..util.dto import PreferenceDto
from ..util.decorator import *
from ..service.preference_service import save_new_preferences

api = PreferenceDto.api
_preference = PreferenceDto.preference

@api.route('/')
class PreferenceList(Resource):
    @token_required
    @api.response(201, 'Preference successfully created.')
    @api.doc('create a new preference')
    @api.expect(_preference, validate=True)
    def post(self, user_pid):
        """Creates a new Preference """
        return save_new_preferences(user_pid=user_pid, data=request.json)