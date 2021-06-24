from app.main.model.specie import Specie
from app.main.model.breed import Breed
from app.main.model.comment import Comment
import uuid
import datetime
from app.main import db
from app.main.model.post import Post
from app.main.model.user import User, circle_member_table, pet_follower_table, post_liker_table
from app.main.model.pet import Pet
from app.main.model.business import Business
from app.main.model.circle import Circle
from app.main.model.pet import post_subject_table
from . import model_save_changes, table_save_changes
from sqlalchemy import func, or_

def save_new_post(user_pid, data):
    new_post_pid = str(uuid.uuid4())
    new_post = Post(
        public_id = new_post_pid,
        content = data.get("content"),
        photo_1 = data.get("photo")[0]["filename"] if len(data.get("photo")) >= 1 else None,
        photo_2 = data.get("photo")[1]["filename"] if len(data.get("photo")) >= 2 else None,
        photo_3 = data.get("photo")[2]["filename"] if len(data.get("photo")) >= 3 else None,
        photo_4 = data.get("photo")[3]["filename"] if len(data.get("photo")) == 4 else None,
        registered_on = datetime.datetime.utcnow(),
        user_creator_id = user_pid,
    )

    if data.get("pinboard_id"):
        business = Business.query.filter_by(public_id=data["pinboard_id"]).first()
        if business:
            new_post.business_pinboard_id = data.get("pinboard_id")
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
            photo = [
                dict(
                    photo_filename = photo
                ) for photo in [
                    post[2], post[3], post[4], post[5]
                ] if photo
            ],
            registered_on = post[6],
            creator_id = post[7],
            creator_name = post[8],
            creator_username = post[9],
            creator_photo = post[10],
            pinboard_id = post[11],
            pinboard_name = post[12],
            pinboard_photo = post[13],
            confiner_id = post[14],
            confiner_name = post[15],
            confiner_photo = post[16],
            subject = [
                dict(
                    subject_id = subject[0],
                    subject_name = subject[1],
                    subject_photo = subject[2],
                    group_id = subject[3],
                    group_name = subject[4],
                    subgroup_id = subject[5],
                    subgroup_name = subject[6],
                    visitor_auth = 3 if db.session.query(
                        pet_follower_table
                    ).filter(
                        pet_follower_table.c.follower_pid == requestor_pid
                    ).filter(
                        pet_follower_table.c.is_owner == True
                    ).filter(
                        pet_follower_table.c.pet_pid == subject[0]
                    ).filter(
                        pet_follower_table.c.is_accepted == True
                    ).first() else 2 if db.session.query(
                        pet_follower_table
                    ).filter(
                        pet_follower_table.c.follower_pid == requestor_pid
                    ).filter(
                        pet_follower_table.c.is_owner == False
                    ).filter(
                        pet_follower_table.c.pet_pid == subject[0]
                    ).filter(
                        pet_follower_table.c.is_accepted == True
                    ).first() else 1 if db.session.query(
                        pet_follower_table
                    ).filter(
                        pet_follower_table.c.follower_pid == requestor_pid
                    ).filter(
                        pet_follower_table.c.is_owner == False
                    ).filter(
                        pet_follower_table.c.pet_pid == subject[0]
                    ).filter(
                        pet_follower_table.c.is_accepted == False
                    ).first() else 0,
                ) for subject in db.session.query(
                    Pet.public_id, 
                    Pet.name,
                    Pet.photo,
                    Specie.public_id,
                    Specie.name,
                    Breed.public_id,
                    Breed.name,
                ).select_from(
                    post_subject_table
                ).filter(
                    post_subject_table.c.post_pid==post[0]
                ).outerjoin(
                    Pet
                ).outerjoin(
                    Breed
                ).outerjoin(
                    Specie
                ).order_by(Pet.registered_on.desc()).all()
            ],
            like_count = db.session.query(
                func.count(post_liker_table.c.public_id)
            ).filter(
                post_liker_table.c.post_pid == post[0]
            ).filter(
                post_liker_table.c.is_unliked == False
            ).scalar(),
            comment_count = Comment.query.filter_by(post_parent_id=post[0]).count(),
            is_liked = 1 if db.session.query(
                post_liker_table
            ).filter(
                post_liker_table.c.post_pid == post[0]
            ).filter(
                post_liker_table.c.liker_pid == requestor_pid
            ).filter(
                post_liker_table.c.is_unliked == False
            ).first() else 0
        ) for post in db.session.query(
            Post.public_id,
            Post.content,
            Post.photo_1,
            Post.photo_2,
            Post.photo_3,
            Post.photo_4,
            Post.registered_on,
            User.public_id,
            User.name,
            User.username,
            User.photo,
            Business.public_id,
            Business.name,
            Business.photo,
            Circle.public_id,
            Circle.name,
            Circle.photo
        ).select_from(
            Post
        ).filter(
            Post.user_creator_id == user_pid
        ).outerjoin(
            User
        ).outerjoin(
            Business
        ).outerjoin(
            Circle
        ).outerjoin(
            circle_member_table
        ).filter(
            or_(Post.circle_confiner_id == None, circle_member_table.c.member_pid == requestor_pid)
        # ).filter(
        #     Post.user_creator_id == User.public_id
        ).order_by(Post.registered_on.desc()).all()
    ]

def get_all_posts_by_business(requestor_pid, business_pid):
    return [
        dict(
            public_id = post[0],
            content = post[1],
            photo = [
                dict(
                    photo_filename = photo
                ) for photo in [
                    post[2], post[3], post[4], post[5]
                ] if photo is not None
            ],
            registered_on = post[6],
            creator_id = post[7],
            creator_name = post[8],
            creator_username = post[9],
            creator_photo = post[10],
            pinboard_id = post[11],
            pinboard_name = post[12],
            pinboard_photo = post[13],
            confiner_id = post[14],
            confiner_name = post[15],
            confiner_photo = post[16],
            subject = [
                dict(
                    subject_id = subject[0],
                    subject_name = subject[1],
                    subject_photo = subject[2],
                    group_id = subject[3],
                    group_name = subject[4],
                    subgroup_id = subject[5],
                    subgroup_name = subject[6],
                    visitor_auth = 3 if db.session.query(
                        pet_follower_table
                    ).filter(
                        pet_follower_table.c.follower_pid == requestor_pid
                    ).filter(
                        pet_follower_table.c.is_owner == True
                    ).filter(
                        pet_follower_table.c.pet_pid == subject[0]
                    ).filter(
                        pet_follower_table.c.is_accepted == True
                    ).first() else 2 if db.session.query(
                        pet_follower_table
                    ).filter(
                        pet_follower_table.c.follower_pid == requestor_pid
                    ).filter(
                        pet_follower_table.c.is_owner == False
                    ).filter(
                        pet_follower_table.c.pet_pid == subject[0]
                    ).filter(
                        pet_follower_table.c.is_accepted == True
                    ).first() else 1 if db.session.query(
                        pet_follower_table
                    ).filter(
                        pet_follower_table.c.follower_pid == requestor_pid
                    ).filter(
                        pet_follower_table.c.is_owner == False
                    ).filter(
                        pet_follower_table.c.pet_pid == subject[0]
                    ).filter(
                        pet_follower_table.c.is_accepted == False
                    ).first() else 0,
                ) for subject in db.session.query(
                    Pet.public_id, 
                    Pet.name,
                    Pet.photo,
                    Specie.public_id,
                    Specie.name,
                    Breed.public_id,
                    Breed.name,
                ).select_from(
                    post_subject_table
                ).filter(
                    post_subject_table.c.post_pid==post[0]
                ).outerjoin(
                    Pet
                ).outerjoin(
                    Breed
                ).outerjoin(
                    Specie
                ).order_by(Pet.registered_on.desc()).all()
            ],
            like_count = db.session.query(
                func.count(post_liker_table.c.public_id)
            ).filter(
                post_liker_table.c.post_pid == post[0]
            ).filter(
                post_liker_table.c.is_unliked == False
            ).scalar(),
            comment_count = Comment.query.filter_by(post_parent_id=post[0]).count(),
            is_liked = 1 if db.session.query(
                post_liker_table
            ).filter(
                post_liker_table.c.post_pid == post[0]
            ).filter(
                post_liker_table.c.liker_pid == requestor_pid
            ).filter(
                post_liker_table.c.is_unliked == False
            ).first() else 0
        ) for post in db.session.query(
            Post.public_id,
            Post.content,
            Post.photo_1,
            Post.photo_2,
            Post.photo_3,
            Post.photo_4,
            Post.registered_on,
            User.public_id,
            User.name,
            User.username,
            User.photo,
            Business.public_id,
            Business.name,
            Business.photo,
            Circle.public_id,
            Circle.name,
            Circle.photo
        ).select_from(
            Post
        ).filter(
            Post.business_pinboard_id == business_pid
        ).outerjoin(
            User
        ).outerjoin(
            Business
        ).outerjoin(
            Circle
        ).order_by(Post.registered_on.desc()).all()
    ]

def get_all_posts_by_pet(user_pid, pet_pid, w_media_only):
    pet = Pet.query.filter_by(public_id=pet_pid).first()
    
    follower = db.session.query(
        pet_follower_table
    ).filter(
        pet_follower_table.c.follower_pid == user_pid
    ).filter(
        pet_follower_table.c.pet_pid == pet_pid
    ).filter(
        pet_follower_table.c.is_accepted == True
    ).first()

    if pet:
        if (follower and pet.is_private == 1) or (pet.is_private == 0):
            return [
                dict(
                    public_id = post[0],
                    content = post[1],
                    photo = [
                        dict(
                            photo_filename = photo
                        ) for photo in [
                            post[2], post[3], post[4], post[5]
                        ] if photo
                    ],
                    registered_on = post[6],
                    creator_id = post[7],
                    creator_name = post[8],
                    creator_username = post[9],
                    creator_photo = post[10],
                    pinboard_id = post[11],
                    pinboard_name = post[12],
                    pinboard_photo = post[13],
                    confiner_id = post[14],
                    confiner_name = post[15],
                    confiner_photo = post[16],
                    subject = [
                        dict(
                            subject_id = subject[0],
                            subject_name = subject[1],
                            subject_photo = subject[2],
                            group_id = subject[3],
                            group_name = subject[4],
                            subgroup_id = subject[5],
                            subgroup_name = subject[6],
                            visitor_auth = 3 if db.session.query(
                                pet_follower_table
                            ).filter(
                                pet_follower_table.c.follower_pid == user_pid
                            ).filter(
                                pet_follower_table.c.is_owner == True
                            ).filter(
                                pet_follower_table.c.pet_pid == subject[0]
                            ).filter(
                                pet_follower_table.c.is_accepted == True
                            ).first() else 2 if db.session.query(
                                pet_follower_table
                            ).filter(
                                pet_follower_table.c.follower_pid == user_pid
                            ).filter(
                                pet_follower_table.c.is_owner == False
                            ).filter(
                                pet_follower_table.c.pet_pid == subject[0]
                            ).filter(
                                pet_follower_table.c.is_accepted == True
                            ).first() else 1 if db.session.query(
                                pet_follower_table
                            ).filter(
                                pet_follower_table.c.follower_pid == user_pid
                            ).filter(
                                pet_follower_table.c.is_owner == False
                            ).filter(
                                pet_follower_table.c.pet_pid == subject[0]
                            ).filter(
                                pet_follower_table.c.is_accepted == False
                            ).first() else 0,
                        ) for subject in db.session.query(
                            Pet.public_id, 
                            Pet.name,
                            Pet.photo,
                            Specie.public_id,
                            Specie.name,
                            Breed.public_id,
                            Breed.name,
                        ).select_from(
                            post_subject_table
                        ).filter(
                            post_subject_table.c.post_pid==post[0]
                        ).outerjoin(
                            Pet
                        ).outerjoin(
                            Breed
                        ).outerjoin(
                            Specie
                        ).order_by(Pet.registered_on.desc()).all()
                    ],
                    like_count = db.session.query(
                        func.count(post_liker_table.c.public_id)
                    ).filter(
                        post_liker_table.c.post_pid == post[0]
                    ).filter(
                        post_liker_table.c.is_unliked == False
                    ).scalar(),
                    comment_count = Comment.query.filter_by(post_parent_id=post[0]).count(),
                    is_liked = 1 if db.session.query(
                        post_liker_table
                    ).filter(
                        post_liker_table.c.post_pid == post[0]
                    ).filter(
                        post_liker_table.c.liker_pid == user_pid
                    ).filter(
                        post_liker_table.c.is_unliked == False
                    ).first() else 0
                ) for post in db.session.query(
                    Post.public_id,
                    Post.content,
                    Post.photo_1,
                    Post.photo_2,
                    Post.photo_3,
                    Post.photo_4,
                    Post.registered_on,
                    User.public_id,
                    User.name,
                    User.username,
                    User.photo,
                    Business.public_id,
                    Business.name,
                    Business.photo,
                    Circle.public_id,
                    Circle.name,
                    Circle.photo
                ).filter(
                    Post.user_creator_id == User.public_id
                ).filter(
                    post_subject_table.c.post_pid == Post.public_id
                ).filter(
                    post_subject_table.c.subject_pid == pet_pid
                ).outerjoin(
                    Business
                ).outerjoin(
                    Circle
                ).outerjoin(
                    circle_member_table
                ).filter(
                    or_(Post.circle_confiner_id == None, circle_member_table.c.member_pid == user_pid)
                ).filter(
                    ((Post.photo_1 != None) if w_media_only == "1" else or_(Post.photo_1 == None, Post.photo_1 != None))
                ).order_by(Post.registered_on.desc()).all()
            ]
        else:
            response_object = {
                'status': 'fail',
                'message': 'Forbidden.'
            }
            return response_object, 403

def get_all_posts_by_circle(requestor_pid, confiner_pid):
    member = db.session.query(
        circle_member_table
    ).filter(
        circle_member_table.c.member_pid == requestor_pid
    ).filter(
        circle_member_table.c.circle_pid == confiner_pid
    ).filter(
        circle_member_table.c.is_accepted == True
    ).first()

    if member:
        return [
            dict(
                public_id = post[0],
                content = post[1],
                photo = [
                    dict(
                        photo_filename = photo
                    ) for photo in [
                        post[2], post[3], post[4], post[5]
                    ] if photo is not None
                ],
                registered_on = post[6],
                creator_id = post[7],
                creator_name = post[8],
                creator_username = post[9],
                creator_photo = post[10],
                pinboard_id = post[11],
                pinboard_name = post[12],
                pinboard_photo = post[13],
                confiner_id = post[14],
                confiner_name = post[15],
                confiner_photo = post[16],
                subject = [
                    dict(
                        subject_id = subject[0],
                        subject_name = subject[1],
                        subject_photo = subject[2],
                        group_id = subject[3],
                        group_name = subject[4],
                        subgroup_id = subject[5],
                        subgroup_name = subject[6],
                        visitor_auth = 3 if db.session.query(
                            pet_follower_table
                        ).filter(
                            pet_follower_table.c.follower_pid == requestor_pid
                        ).filter(
                            pet_follower_table.c.is_owner == True
                        ).filter(
                            pet_follower_table.c.pet_pid == subject[0]
                        ).filter(
                            pet_follower_table.c.is_accepted == True
                        ).first() else 2 if db.session.query(
                            pet_follower_table
                        ).filter(
                            pet_follower_table.c.follower_pid == requestor_pid
                        ).filter(
                            pet_follower_table.c.is_owner == False
                        ).filter(
                            pet_follower_table.c.pet_pid == subject[0]
                        ).filter(
                            pet_follower_table.c.is_accepted == True
                        ).first() else 1 if db.session.query(
                            pet_follower_table
                        ).filter(
                            pet_follower_table.c.follower_pid == requestor_pid
                        ).filter(
                            pet_follower_table.c.is_owner == False
                        ).filter(
                            pet_follower_table.c.pet_pid == subject[0]
                        ).filter(
                            pet_follower_table.c.is_accepted == False
                        ).first() else 0,
                    ) for subject in db.session.query(
                        Pet.public_id, 
                        Pet.name,
                        Pet.photo,
                        Specie.public_id,
                        Specie.name,
                        Breed.public_id,
                        Breed.name,
                    ).select_from(
                        post_subject_table
                    ).filter(
                        post_subject_table.c.post_pid==post[0]
                    ).outerjoin(
                        Pet
                    ).outerjoin(
                        Breed
                    ).outerjoin(
                        Specie
                    ).order_by(Pet.registered_on.desc()).all()
                ],
                like_count = db.session.query(
                    func.count(post_liker_table.c.public_id)
                ).filter(
                    post_liker_table.c.post_pid == post[0]
                ).filter(
                    post_liker_table.c.is_unliked == False
                ).scalar(),
                comment_count = Comment.query.filter_by(post_parent_id=post[0]).count(),
                is_liked = 1 if db.session.query(
                    post_liker_table
                ).filter(
                    post_liker_table.c.post_pid == post[0]
                ).filter(
                    post_liker_table.c.liker_pid == requestor_pid
                ).filter(
                    post_liker_table.c.is_unliked == False
                ).first() else 0
            ) for post in db.session.query(
                Post.public_id,
                Post.content,
                Post.photo_1,
                Post.photo_2,
                Post.photo_3,
                Post.photo_4,
                Post.registered_on,
                User.public_id,
                User.name,
                User.username,
                User.photo,
                Business.public_id,
                Business.name,
                Business.photo,
                Circle.public_id,
                Circle.name,
                Circle.photo
            ).select_from(
                Post
            ).filter(
                Post.circle_confiner_id == confiner_pid
            ).outerjoin(
                User
            ).outerjoin(
                Business
            ).outerjoin(
                Circle
            ).order_by(Post.registered_on.desc()).all()
        ]

    else:
        response_object = {
            'status': 'fail',
            'message': 'Forbidden.'
        }
        return response_object, 403

def get_all_posts(requestor_pid):
    return [
        dict(
            public_id = post[0],
            content = post[1],
            photo = [
                dict(
                    photo_filename = photo
                ) for photo in [
                    post[2], post[3], post[4], post[5]
                ] if photo is not None
            ],
            registered_on = post[6],
            creator_id = post[7],
            creator_name = post[8],
            creator_username = post[9],
            creator_photo = post[10],
            pinboard_id = post[11],
            pinboard_name = post[12],
            pinboard_photo = post[13],
            confiner_id = post[14],
            confiner_name = post[15],
            confiner_photo = post[16],
            subject = [
                dict(
                    subject_id = subject[0],
                    subject_name = subject[1],
                    subject_photo = subject[2],
                    group_id = subject[3],
                    group_name = subject[4],
                    subgroup_id = subject[5],
                    subgroup_name = subject[6],
                    visitor_auth = 3 if db.session.query(
                        pet_follower_table
                    ).filter(
                        pet_follower_table.c.follower_pid == requestor_pid
                    ).filter(
                        pet_follower_table.c.is_owner == True
                    ).filter(
                        pet_follower_table.c.pet_pid == subject[0]
                    ).filter(
                        pet_follower_table.c.is_accepted == True
                    ).first() else 2 if db.session.query(
                        pet_follower_table
                    ).filter(
                        pet_follower_table.c.follower_pid == requestor_pid
                    ).filter(
                        pet_follower_table.c.is_owner == False
                    ).filter(
                        pet_follower_table.c.pet_pid == subject[0]
                    ).filter(
                        pet_follower_table.c.is_accepted == True
                    ).first() else 1 if db.session.query(
                        pet_follower_table
                    ).filter(
                        pet_follower_table.c.follower_pid == requestor_pid
                    ).filter(
                        pet_follower_table.c.is_owner == False
                    ).filter(
                        pet_follower_table.c.pet_pid == subject[0]
                    ).filter(
                        pet_follower_table.c.is_accepted == False
                    ).first() else 0,
                ) for subject in db.session.query(
                    Pet.public_id, 
                    Pet.name,
                    Pet.photo,
                    Specie.public_id,
                    Specie.name,
                    Breed.public_id,
                    Breed.name,
                ).select_from(
                    post_subject_table
                ).filter(
                    post_subject_table.c.post_pid==post[0]
                ).outerjoin(
                    Pet
                ).outerjoin(
                    Breed
                ).outerjoin(
                    Specie
                ).order_by(Pet.registered_on.desc()).all()
            ],
            like_count = db.session.query(
                func.count(post_liker_table.c.public_id)
            ).filter(
                post_liker_table.c.post_pid == post[0]
            ).filter(
                post_liker_table.c.is_unliked == False
            ).scalar(),
            comment_count = Comment.query.filter_by(post_parent_id=post[0]).count(),
            is_liked = 1 if db.session.query(
                post_liker_table
            ).filter(
                post_liker_table.c.post_pid == post[0]
            ).filter(
                post_liker_table.c.liker_pid == requestor_pid
            ).filter(
                post_liker_table.c.is_unliked == False
            ).first() else 0
        ) for post in db.session.query(
            Post.public_id,
            Post.content,
            Post.photo_1,
            Post.photo_2,
            Post.photo_3,
            Post.photo_4,
            Post.registered_on,
            User.public_id,
            User.name,
            User.username,
            User.photo,
            Business.public_id,
            Business.name,
            Business.photo,
            Circle.public_id,
            Circle.name,
            Circle.photo,
            func.count(post_subject_table.c.subject_pid)
        ).select_from(
            Post
        ).outerjoin(
            User
        ).outerjoin(
            post_subject_table
        ).outerjoin(
            Pet
        ).outerjoin(
            pet_follower_table
        ).filter(
            pet_follower_table.c.is_accepted == True
        ).filter(
            pet_follower_table.c.follower_pid == requestor_pid
        ).outerjoin(
            Business
        ).outerjoin(
            Circle
        ).outerjoin(
            circle_member_table
        ).filter(
            or_(Post.circle_confiner_id == None, circle_member_table.c.member_pid == requestor_pid)
        ).group_by(
            Post.public_id,
            Post.content,
            Post.photo_1,
            Post.photo_2,
            Post.photo_3,
            Post.photo_4,
            Post.registered_on,
            User.public_id,
            User.name,
            User.username,
            User.photo,
            Business.public_id,
            Business.name,
            Business.photo,
            Circle.public_id,
            Circle.name,
            Circle.photo
        ).order_by(Post.registered_on.desc()).all()
    ]

def get_a_post(requestor_pid, public_id):
    post = db.session.query(
        Post.public_id,
        Post.content,
        Post.photo_1,
        Post.photo_2,
        Post.photo_3,
        Post.photo_4,
        Post.registered_on,
        User.public_id,
        User.name,
        User.username,
        User.photo,
        Business.public_id,
        Business.name,
        Business.photo,
        Circle.public_id,
        Circle.name,
        Circle.photo
    ).filter(
        Post.public_id == public_id
    ).filter(
        Post.user_creator_id == User.public_id
    ).first()

    if post:
        return dict(
            public_id = post[0],
            content = post[1],
            photo = [
                dict(
                    photo_filename = photo
                ) for photo in [
                    post[2], post[3], post[4], post[5]
                ] if photo
            ],
            registered_on = post[6],
            creator_id = post[7],
            creator_name = post[8],
            creator_username = post[9],
            creator_photo = post[10],
            pinboard_id = post[11],
            pinboard_name = post[12],
            pinboard_photo = post[13],
            confiner_id = post[14],
            confiner_name = post[15],
            confiner_photo = post[16],
            subject = [
                dict(
                    subject_id = subject[0],
                    subject_name = subject[1],
                    subject_photo = subject[2],
                    group_id = subject[3],
                    group_name = subject[4],
                    subgroup_id = subject[5],
                    subgroup_name = subject[6],
                    visitor_auth = 3 if db.session.query(
                        pet_follower_table
                    ).filter(
                        pet_follower_table.c.follower_pid == requestor_pid
                    ).filter(
                        pet_follower_table.c.is_owner == True
                    ).filter(
                        pet_follower_table.c.pet_pid == subject[0]
                    ).filter(
                        pet_follower_table.c.is_accepted == True
                    ).first() else 2 if db.session.query(
                        pet_follower_table
                    ).filter(
                        pet_follower_table.c.follower_pid == requestor_pid
                    ).filter(
                        pet_follower_table.c.is_owner == False
                    ).filter(
                        pet_follower_table.c.pet_pid == subject[0]
                    ).filter(
                        pet_follower_table.c.is_accepted == True
                    ).first() else 1 if db.session.query(
                        pet_follower_table
                    ).filter(
                        pet_follower_table.c.follower_pid == requestor_pid
                    ).filter(
                        pet_follower_table.c.is_owner == False
                    ).filter(
                        pet_follower_table.c.pet_pid == subject[0]
                    ).filter(
                        pet_follower_table.c.is_accepted == False
                    ).first() else 0,
                ) for subject in db.session.query(
                    Pet.public_id, 
                    Pet.name,
                    Pet.photo,
                    Specie.public_id,
                    Specie.name,
                    Breed.public_id,
                    Breed.name,
                ).select_from(
                    post_subject_table
                ).filter(
                    post_subject_table.c.post_pid==post[0]
                ).outerjoin(
                    Pet
                ).outerjoin(
                    Breed
                ).outerjoin(
                    Specie
                ).order_by(Pet.registered_on.desc()).all()
            ],
            like_count = db.session.query(
                func.count(post_liker_table.c.public_id)
            ).filter(
                post_liker_table.c.post_pid == post[0]
            ).filter(
                post_liker_table.c.is_unliked == False
            ).scalar(),
            comment_count = Comment.query.filter_by(post_parent_id=post[0]).count(),
            is_liked = 1 if db.session.query(
                post_liker_table
            ).filter(
                post_liker_table.c.post_pid == post[0]
            ).filter(
                post_liker_table.c.liker_pid == requestor_pid
            ).filter(
                post_liker_table.c.is_unliked == False
            ).first() else 0
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

def like_a_post(requestor_pid, post_pid):
    post = Post.query.filter_by(public_id=post_pid).first()

    if post:
        this_like = db.session.query(
            post_liker_table
        ).filter(
            post_liker_table.c.post_pid == post_pid
        ).filter(
            post_liker_table.c.liker_pid == requestor_pid
        ).first()

        if not this_like:
            statement = post_liker_table.insert().values(
                public_id=str(uuid.uuid4()),
                post_pid=post_pid,
                liker_pid=requestor_pid
            )
            table_save_changes(statement)
            response_object = {
                'status': 'success',
                'message': 'Post successfully liked.'
            }
            return response_object, 201
        else:
            statement = post_liker_table.update().where(
                post_liker_table.c.post_pid==post_pid
            ).where(
                post_liker_table.c.liker_pid==requestor_pid
            ).values(
                is_unliked = True if this_like.is_unliked is False else False
            )
            table_save_changes(statement)
            response_object = {
                'status': 'success',
                'message': 'Post successfully {}.'.format("liked" if this_like.is_unliked is False else "unliked")
            }
            return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'No post found.'
        }
        return response_object, 404