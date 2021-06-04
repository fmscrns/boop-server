from operator import pos
import uuid
import datetime
from sqlalchemy.sql.expression import select

from sqlalchemy.sql.functions import user
from app.main import db
from app.main.model.post import Post
from app.main.model.user import User, circle_member_table
from app.main.model.pet import Pet
from app.main.model.business import Business
from app.main.model.circle import Circle
from app.main.model.pet import post_subject_table
from . import model_save_changes, table_save_changes
from sqlalchemy import or_

def save_new_post(user_pid, data):
    new_post_pid = str(uuid.uuid4())
    new_post = Post(
        public_id = new_post_pid,
        content = data.get("content"),
        photo = data.get("photo"),
        registered_on = datetime.datetime.utcnow(),
        user_creator_id = user_pid,
    )

    if data.get("pinboard_id"):
        business = Business.query.filter_by(public_id=data["pinboard_id"]).first()
        if business:
            if business.user_executive_id == user_pid:
                new_post.business_pinboard_id = data.get("pinboard_id")
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Unauthorized.'
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'No business found.'
            }
            return response_object, 404

    if data.get("confiner_id"):
        circle = Circle.query.filter_by(public_id=data["confiner_id"]).first()
        if circle:
            member = db.session.query(
                circle_member_table
            ).filter(
                circle_member_table.c.circle_pid==data["confiner_id"]
            ).filter(
                circle_member_table.c.member_pid==user_pid
            ).first()
        
            if member:
                new_post.circle_confiner_id = data.get("confiner_id")
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Unauthorized.'
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'No circle found.'
            }
            return response_object, 404
            
    model_save_changes(new_post)

    for subject in data.get("subject"):
        statement = post_subject_table.insert().values(
            public_id = str(uuid.uuid4()),
            post_pid = new_post_pid,
            subject_pid = subject["public_id"]
        )
        table_save_changes(statement)

    response_object = {
        'status': 'success',
        'message': 'Post successfully registered.'
    }
    return response_object, 201

def get_all_posts_by_user(requestor_pid, user_pid):
    return [
        dict(
            public_id = post[0],
            content = post[1],
            photo = post[2],
            registered_on = post[3],
            creator_id = post[4],
            creator_name = post[5],
            creator_username = post[6],
            creator_photo = post[7],
            pinboard_id = post[8],
            pinboard_name = post[9],
            confiner_id = post[10],
            confiner_name = post[11],
            subject = [
                dict(
                    subject_id = subject[0],
                    subject_name = subject[1],
                    subject_photo = subject[2]
                ) for subject in db.session.query(
                    Pet.public_id, 
                    Pet.name,
                    Pet.photo
                    ).filter(post_subject_table.c.post_pid==post[0]
                    ).filter(post_subject_table.c.subject_pid==Pet.public_id
                    ).all()
            ],
        ) for post in db.session.query(
            Post.public_id,
            Post.content,
            Post.photo,
            Post.registered_on,
            User.public_id,
            User.name,
            User.username,
            User.photo,
            Business.public_id,
            Business.name,
            Circle.public_id,
            Circle.name
        ).select_from(
            Post
        ).filter(
            Post.user_creator_id == user_pid
        ).outerjoin(
            Business
        ).outerjoin(
            Circle
        ).outerjoin(
            circle_member_table
        ).filter(
            or_(Post.circle_confiner_id == None, circle_member_table.c.member_pid == requestor_pid)
        ).filter(
            Post.user_creator_id == User.public_id
        ).order_by(Post.registered_on.desc()).all()
    ]

def get_all_posts_by_user2(requestor_pid, user_pid):
    return [
        dict(
            public_id = post[0],
            content = post[1],
            photo = post[2],
            registered_on = post[3],
            creator_id = post[4],
            creator_name = post[5],
            creator_username = post[6],
            creator_photo = post[7],
            pinboard_id = post[8],
            pinboard_name = post[9],
            confiner_id = post[10],
            confiner_name = post[11],
            subject = [
                dict(
                    subject_id = subject[0],
                    subject_name = subject[1],
                    subject_photo = subject[2]
                ) for subject in db.session.query(
                    Pet.public_id, 
                    Pet.name,
                    Pet.photo
                    ).filter(post_subject_table.c.post_pid==post[0]
                    ).filter(post_subject_table.c.subject_pid==Pet.public_id
                    ).all()
            ],
        ) for post in db.session.query(
            Post.public_id,
            Post.content,
            Post.photo,
            Post.registered_on,
            User.public_id,
            User.name,
            User.username,
            User.photo,
            Business.public_id,
            Business.name,
            Circle.public_id,
            Circle.name
        ).filter(
            Post.user_creator_id == user_pid
        ).filter(
            Post.user_creator_id == User.public_id
        ).filter(
            Post.business_pinboard_id == Business.public_id
        ).outerjoin(
            Circle
        ).outerjoin(
            circle_member_table
        ).filter(
            or_(Post.circle_confiner_id == None, circle_member_table.c.member_pid == user_pid)
        ).order_by(Post.registered_on.desc()).all()
    ]

def get_all_posts_by_business(business_pid):
    return [
        dict(
            public_id = post[0],
            content = post[1],
            photo = post[2],
            registered_on = post[3],
            creator_id = post[4],
            creator_name = post[5],
            creator_username = post[6],
            creator_photo = post[7],
            subject = [
                dict(
                    subject_id = subject[0],
                    subject_name = subject[1],
                    subject_photo = subject[2]
                ) for subject in db.session.query(
                    Pet.public_id, 
                    Pet.name,
                    Pet.photo
                    ).filter(post_subject_table.c.post_pid==post[0]
                    ).filter(post_subject_table.c.subject_pid==Pet.public_id
                    ).all()
            ]
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
            Post.business_pinboard_id == business_pid
        ).filter(
            Post.user_creator_id == User.public_id
        ).order_by(Post.registered_on.desc()).all()
    ]

def get_all_posts_by_pet(user_pid, pet_pid):
    return [
        dict(
            public_id = post[0],
            content = post[1],
            photo = post[2],
            registered_on = post[3],
            creator_id = post[4],
            creator_name = post[5],
            creator_username = post[6],
            creator_photo = post[7],
            subject = [
                dict(
                    subject_id = subject[0],
                    subject_name = subject[1],
                    subject_photo = subject[2]
                ) for subject in db.session.query(
                    Pet.public_id, 
                    Pet.name,
                    Pet.photo
                    ).filter(post_subject_table.c.post_pid==post[0]
                    ).filter(post_subject_table.c.subject_pid==Pet.public_id
                    ).all()
            ]
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
        ).filter(
            post_subject_table.c.post_pid == Post.public_id
        ).filter(
            post_subject_table.c.subject_pid == pet_pid
        ).outerjoin(
            Circle
        ).outerjoin(
            circle_member_table
        ).filter(
            or_(Post.circle_confiner_id == None, circle_member_table.c.member_pid == user_pid)
        ).order_by(Post.registered_on.desc()).all()
    ]

def get_all_posts_by_circle(confiner_pid):
    return [
        dict(
            public_id = post[0],
            content = post[1],
            photo = post[2],
            registered_on = post[3],
            creator_id = post[4],
            creator_name = post[5],
            creator_username = post[6],
            creator_photo = post[7],
            subject = [
                dict(
                    subject_id = subject[0],
                    subject_name = subject[1],
                    subject_photo = subject[2]
                ) for subject in db.session.query(
                    Pet.public_id, 
                    Pet.name,
                    Pet.photo
                    ).filter(post_subject_table.c.post_pid==post[0]
                    ).filter(post_subject_table.c.subject_pid==Pet.public_id
                    ).all()
            ]
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
            Post.circle_confiner_id == confiner_pid
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
            creator_photo = post[7],
            subject = [
                dict(
                    subject_id = subject[0],
                    subject_name = subject[1],
                    subject_photo = subject[2]
                ) for subject in db.session.query(
                    Pet.public_id, 
                    Pet.name,
                    Pet.photo
                    ).filter(post_subject_table.c.post_pid==post[0]
                    ).filter(post_subject_table.c.subject_pid==Pet.public_id
                    ).all()
            ]
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
        ).filter(
            Post.business_pinboard_id == None
        ).filter(
            Post.circle_confiner_id == None
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
            creator_photo = post[7],
            subject = [
                dict(
                    subject_id = subject[0],
                    subject_name = subject[1],
                    subject_photo = subject[2]
                ) for subject in db.session.query(
                    Pet.public_id, 
                    Pet.name,
                    Pet.photo
                    ).filter(post_subject_table.c.post_pid==post[0]
                    ).filter(post_subject_table.c.subject_pid==Pet.public_id
                    ).all()
            ]
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