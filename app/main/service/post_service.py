import uuid
import datetime

from app.main import db
from app.main.model.post import Post
from app.main.model.user import User

def save_new_post(user_pid, data):
    new_post = Post(
        public_id = str(uuid.uuid4()),
        content = data.get("content"),
        photo = data.get("photo"),
        registered_on = datetime.datetime.utcnow(),
        user_creator_id = user_pid
    )
    save_changes(new_post)
    response_object = {
        'status': 'success',
        'message': 'Post successfully registered.',
        'payload': User.query.filter_by(public_id=user_pid).first().username
    }
    return response_object, 201

def get_all_posts_by_user(user_pid):
    return [
        dict(
            public_id = post[0],
            content = post[1],
            photo = post[2],
            registered_on = post[3],
            creator_id = post[4],
            creator_name = post[5],
            creator_username = post[6],
            creator_photo = post[7]
        ) for post in db.session.query(
            Post.public_id,
            Post.content,
            Post.photo,
            Post.registered_on,
            User.public_id,
            User.name,
            User.username,
            User.photo
        ).filter(
            Post.user_creator_id == user_pid
        ).filter(
            Post.user_creator_id == User.public_id
        ).order_by(Post.registered_on.desc()).all()
    ]

def get_all_posts():
    return [
        dict(
            public_id = post[0],
            content = post[1],
            photo = post[2],
            registered_on = post[3],
            creator_id = post[4],
            creator_name = post[5],
            creator_username = post[6],
            creator_photo = post[7]
        ) for post in db.session.query(
            Post.public_id,
            Post.content,
            Post.photo,
            Post.registered_on,
            User.public_id,
            User.name,
            User.username,
            User.photo
        ).filter(
            Post.user_creator_id == User.public_id
        ).order_by(Post.registered_on.desc()).all()
    ]

def get_a_post(public_id):
    post = db.session.query(
        Post.public_id,
        Post.content,
        Post.photo,
        Post.registered_on,
        User.public_id,
        User.name,
        User.username,
        User.photo
    ).filter(
        Post.public_id == public_id
    ).filter(
        Post.user_creator_id == User.public_id
    ).first()

    if post:
        return dict(
            public_id = post[0],
            content = post[1],
            photo = post[2],
            registered_on = post[3],
            creator_id = post[4],
            creator_name = post[5],
            creator_username = post[6],
            creator_photo = post[7]
        )

def delete_a_post(public_id, user_pid):
    post = Post.query.filter_by(public_id=public_id).first()
    if post:
        if post.user_creator_id == user_pid:
            db.session.delete(post)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Post successfully deleted.'
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
            'message': 'No post found.'
        }
        return response_object, 404

def save_changes(data):
    db.session.add(data)
    db.session.commit()