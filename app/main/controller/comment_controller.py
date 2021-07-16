from flask import request
from flask_restx import Resource
from ..util.dto import CommentDto
from ..util.decorator import *
from ..service.comment_service import save_new_comment, get_all_comments_by_user, delete_a_comment, get_all_comments_by_post

api = CommentDto.api
_comment = CommentDto.comment

@api.route('/')
class CommentList(Resource):
    @token_required
    @api.response(201, 'Comment successfully created.')
    @api.doc('create a new comment')
    @api.expect(_comment, validate=True)
    def post(self, user_pid):
        """Creates a new Comment """
        data = request.json
        return save_new_comment(user_pid=user_pid, data=data)

@api.route('/creator/<creator_id>')
@api.param("creator_id", "The User public identifier")
class CommentListByUser(Resource):
    @token_required
    @api.doc('list_of_registered_comments')
    @api.marshal_list_with(_comment, envelope='data')
    def get(self, user_pid, creator_id):
        """List all registered comments"""
        return get_all_comments_by_user(user_pid, creator_id)

@api.route('/parent/<parent_id>')
@api.param("parent_id", "The Pet public identifier")
class CommentListByPost(Resource):
    @token_required
    @api.doc('list_of_registered_comments')
    @api.marshal_list_with(_comment, envelope='data')
    def get(self, user_pid, parent_id):
        """List all registered comments"""
        return get_all_comments_by_post(user_pid, parent_id, request.args.get("pagination_no", type=int))

@api.route('/<public_id>')
@api.param('public_id', 'The Comment identifier')
@api.response(404, 'Comment not found.')
class Comment(Resource):
    @token_required
    @api.response(201, 'Comment successfully deleted.')
    @api.doc('delete a comment')
    def delete(self, user_pid, public_id):
        """delete a comment given its identifier"""
        return delete_a_comment(public_id, user_pid)