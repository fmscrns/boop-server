from flask import request
from flask_restx import Resource

from ..util.dto import NotificationDto
from ..util.decorator import *
from ..service.notification_service import get_all_notifications_by_user, get_a_notification

api = NotificationDto.api
_notification = NotificationDto.notification

@api.route('/')
class NotificationListByUser(Resource):
    @token_required
    @api.doc('list_of_registered_notifications_by_user_recipient')
    @api.marshal_list_with(_notification, envelope='data')
    def get(self, user_pid):
        """List all registered notifications"""
        return get_all_notifications_by_user(user_pid, request.args.get("read"), request.args.get("count"))

@api.route('/<public_id>')
@api.param('public_id', 'The Notification identifier')
@api.response(404, 'Notification not found.')
class Notification(Resource):
    @token_required
    @api.doc('get a notification')
    @api.marshal_with(_notification)
    def get(self, public_id):
        """get a notification given its identifier"""
        notification = get_a_notification(public_id)
        if not notification:
            api.abort(404)
        else:
            return notification