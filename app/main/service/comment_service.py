from flask.globals import current_app
from app.main.service import notification_service
from app.main.model.comment import Comment
import uuid
import datetime
from app.main import db
from app.main.model.post import Post
from app.main.model.user import User, circle_member_table
from app.main.model.circle import Circle
from . import model_save_changes
from sqlalchemy import or_

def save_new_comment(user_pid, data):
    post = Post.query.filter_by(public_id=data.get("parent_id")).first()

    if post:
        new_comment = Comment(
            public_id = str(uuid.uuid4()),
            content = data.get("content"),
            photo = data.get("photo")[0]["filename"],
            registered_on = datetime.datetime.utcnow(),
            user_creator_id = user_pid,
            post_parent_id = data.get("parent_id")
        )     
        model_save_changes(new_comment)

        if post.user_creator_id != user_pid:
            notification_service.save_new_notification(
                "{} commented on your post.".format(User.query.filter_by(public_id=user_pid).first().name),
                0,
                user_pid,
                post.user_creator_id,
                post_subject_id = post.public_id
            )

        response_object = {
            'status': 'success',
            'message': 'Comment successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Post does not exist.'
        }
        return response_object, 404

def get_all_comments_by_user(requestor_pid, user_pid):
    return [
        dict(
            public_id = comment[0],
            content = comment[1],
            photo = comment[2],
            registered_on = comment[3],
            creator_id = comment[4],
            creator_name = comment[5],
            creator_username = comment[6],
            creator_photo = comment[7],
            parent_id = comment[8]
        ) for comment in db.session.query(
            Comment.public_id,
            Comment.content,
            Comment.photo,
            Comment.registered_on,
            User.public_id,
            User.name,
            User.username,
            User.photo,
            Post.public_id
        ).select_from(
            Comment
        ).filter(
            Comment.user_creator_id == user_pid
        ).outerjoin(
            User
        ).outerjoin(
            Post
        ).outerjoin(
            Circle
        ).outerjoin(
            circle_member_table
        ).filter(
            or_(Post.circle_confiner_id == None, circle_member_table.c.member_pid == requestor_pid)
        ).order_by(Comment.registered_on.desc()).all()
    ]

def get_all_comments_by_post(user_pid, post_pid, pagination_no):
    try:
        return [
            dict(
                public_id = comment[0],
                content = comment[1],
                registered_on = comment[2],
                creator_id = comment[3],
                creator_name = comment[4],
                creator_username = comment[5],
                creator_photo = comment[6],
                parent_id = comment[7],
                photo = [
                    dict(
                        photo_filename = comment[8]
                    )
                ] if comment[8] else None
            ) for comment in db.session.query(
                Comment.public_id,
                Comment.content,
                Comment.registered_on,
                User.public_id,
                User.name,
                User.username,
                User.photo,
                Post.public_id,
                Comment.photo
            ).select_from(
                Comment
            ).filter(
                Comment.user_creator_id == User.public_id
            ).outerjoin(
                Post
            ).filter(
                Post.public_id == post_pid
            ).order_by(Comment.registered_on.desc()
            ).paginate(
                page=pagination_no,
                per_page=current_app.config["PER_PAGE_PAGINATION"]
            ).items
        ]
    except:
        pass

def delete_a_comment(public_id, user_pid):
    comment = Comment.query.filter_by(public_id=public_id).first()
    if comment:
        if comment.user_creator_id == user_pid:
            db.session.delete(comment)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Comment successfully deleted.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Not match or no authorization.'
            }
            return response_object, 400
    else:
        response_object = {
            'status': 'fail',
            'message': 'No comment found.'
        }
        return response_object, 404