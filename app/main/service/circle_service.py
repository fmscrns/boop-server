from sqlalchemy.sql.expression import outerjoin, text
from sqlalchemy.sql.functions import func, user
from app.main.model.preference import Preference
from flask.globals import current_app
from sqlalchemy import not_
from app.main.model.notification import Notification
import uuid
import datetime
from app.main import db
from app.main.model.circle import Circle, circle_type_table
from app.main.model.circle_type import CircleType
from app.main.model.user import User, circle_member_table
from app.main.service import model_save_changes, notification_service, table_save_changes

def save_new_circle(user_pid, data):
    try:
        circle_pid = str(uuid.uuid4())
        new_circle = Circle(
            public_id = circle_pid,
            name = data.get("name"),
            bio = data.get("bio"),
            photo = data.get("photo"),
            registered_on = datetime.datetime.utcnow()
        )
        model_save_changes(new_circle)
        for _type in data.get("_type"):
            statement = circle_type_table.insert().values(
                public_id = str(uuid.uuid4()),
                circle_pid = circle_pid,
                type_pid = _type["public_id"]
            )
            table_save_changes(statement)
        statement = circle_member_table.insert().values(
            public_id = str(uuid.uuid4()),
            circle_pid = circle_pid,
            member_pid = user_pid,
            is_accepted = True,
            is_admin = True
        )
        table_save_changes(statement)
        response_object = {
            'status': 'success',
            'message': 'Circle successfully registered.',
            'public_id': circle_pid
        }
        return response_object, 201
    except:
        return 500

def get_all_circles_by_user(requestor_pid, user_pid):
    if requestor_pid == user_pid:
        return [
            dict(
                public_id = circle[0],
                name = circle[1],
                bio = circle[2],
                _type = [
                    dict(
                        type_pid = _type[0],
                        type_name = _type[1]
                    ) for _type in db.session.query(
                        circle_type_table.c.type_pid, 
                        CircleType.name
                        ).filter(circle_type_table.c.circle_pid==circle[0]
                        ).filter(circle_type_table.c.type_pid==CircleType.public_id
                        ).all()
                ],
                photo = circle[3],
                registered_on = circle[4],
                member_count = circle[5],
                admin = [
                    dict(
                        admin_id = admin[0],
                        admin_name = admin[1],
                        admin_username = admin[2],
                        admin_photo = admin[3],
                    ) for admin in db.session.query(
                        User.public_id,
                        User.name,
                        User.username,
                        User.photo
                    ).filter(circle_member_table.c.member_pid==User.public_id
                    ).filter(circle_member_table.c.is_admin==True
                    ).filter(circle_member_table.c.circle_pid==circle[0]
                    ).all()
                ]
            ) for circle in db.session.query(
                Circle.public_id,
                Circle.name,
                Circle.bio,
                Circle.photo,
                Circle.registered_on,
                func.count(circle_member_table.c.circle_pid).filter(circle_member_table.c.is_admin == None).label("member_count")
            ).select_from(
                circle_member_table
            ).filter(
                circle_member_table.c.member_pid == requestor_pid
            ).filter(
                circle_member_table.c.is_accepted == True
            ).outerjoin(
                Circle
            ).group_by(
                Circle.public_id,
                Circle.name,
                Circle.bio,
                Circle.photo,
                Circle.registered_on
            ).order_by(Circle.registered_on.desc()).all()
        ]
    else:
        response_object = {
            'status': 'fail',
            'message': 'Forbidden.'
        }
        return response_object, 403

def get_all_circles_by_preference(requestor_pid, pagination_no):
    return [
        dict(
            public_id = circle[0],
            name = circle[1],
            bio = circle[2],
            _type = [
                dict(
                    type_pid = _type[0],
                    type_name = _type[1]
                ) for _type in db.session.query(
                    circle_type_table.c.type_pid, 
                    CircleType.name
                    ).filter(circle_type_table.c.circle_pid==circle[0]
                    ).filter(circle_type_table.c.type_pid==CircleType.public_id
                    ).all()
            ],
            photo = circle[3],
            registered_on = circle[4],
            member_count = circle[5],
            admin = [
                dict(
                    admin_id = admin[0],
                    admin_name = admin[1],
                    admin_username = admin[2],
                    admin_photo = admin[3],
                ) for admin in db.session.query(
                    User.public_id,
                    User.name,
                    User.username,
                    User.photo
                ).filter(circle_member_table.c.member_pid==User.public_id
                ).filter(circle_member_table.c.is_admin==True
                ).filter(circle_member_table.c.circle_pid==circle[0]
                ).all()
            ]
        ) for circle in db.session.query(
            Circle.public_id,
            Circle.name,
            Circle.bio,
            Circle.photo,
            Circle.registered_on,
            func.count(circle_member_table.c.circle_pid).filter(circle_member_table.c.is_admin == None).label("member_count")
        ).select_from(
            Circle
        ).filter(
            not_(
                Circle.public_id.in_(
                    db.session.query(
                        circle_member_table.c.circle_pid
                    ).select_from(
                        circle_member_table
                    ).outerjoin(
                        Circle
                    ).outerjoin(
                        User
                    ).filter(
                        User.public_id == requestor_pid
                    ).subquery()
                )
            )
        ).outerjoin(
            circle_type_table
        ).outerjoin(
            CircleType
        ).outerjoin(
            Preference
        ).filter(
            Preference.user_selector_id == requestor_pid)
        .outerjoin(
            circle_member_table
        ).group_by(
            Circle.public_id,
            Circle.name,
            Circle.bio,
            Circle.photo,
            Circle.registered_on
        ).order_by(
            text("member_count DESC")
        ).paginate(
            page=pagination_no,
            per_page=current_app.config["PER_PAGE_PAGINATION"]
        ).items
    ]

def patch_a_circle(public_id, user_pid, data):
    circle = Circle.query.filter_by(public_id=public_id).first()
    admin = db.session.query(
        circle_member_table
    ).filter(
        circle_member_table.c.circle_pid == public_id
    ).filter(
        circle_member_table.c.member_pid == user_pid
    ).filter(
        circle_member_table.c.is_admin == True
    ).first()

    admin_list = db.session.query(
        circle_member_table.c.member_pid
    ).filter(
        circle_member_table.c.circle_pid == public_id
    ).filter(
        circle_member_table.c.is_admin == True
    ).all()

    if circle:
        if admin:
            statement = circle_type_table.delete().where(
                circle_type_table.c.circle_pid==circle.public_id)
            table_save_changes(statement)
            for _type in data.get("_type"):
                statement = circle_type_table.insert().values(
                    public_id = str(uuid.uuid4()),
                    circle_pid = circle.public_id,
                    type_pid = _type["public_id"]
                )
                table_save_changes(statement)
            old_circle_name = circle.name
            circle.name = data.get("name")
            circle.bio = data.get("bio")
            circle.photo = data.get("photo")
            db.session.commit()

            for _admin in admin_list:
                if _admin[0] != user_pid:
                    notification_service.save_new_notification(
                        "{} {} {}.".format(
                            User.query.filter_by(public_id=user_pid).first().name,
                            "has made some updates on",
                            old_circle_name
                        ),
                        0,
                        user_pid,
                        _admin[0],
                        circle_subject_id = circle.public_id
                    )

            response_object = {
                'status': 'success',
                'message': 'Circle successfully updated.'
            }
            return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'No circle found.'
        }
        return response_object, 404

def delete_a_circle(public_id, user_pid, data):
    circle = Circle.query.filter_by(public_id=public_id).first()
    admin = db.session.query(
        circle_member_table
    ).filter(
        circle_member_table.c.circle_pid == public_id
    ).filter(
        circle_member_table.c.member_pid == user_pid
    ).filter(
        circle_member_table.c.is_admin == True
    ).first()
    if circle:
        if admin and data.get("name") == circle.name:
            db.session.delete(circle)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Circle successfully deleted.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Not match or no authorization.'
            }
            return response_object, 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'No circle found.'
        }
        return response_object, 404

def get_all_circles():
    return Circle.query.all()

def get_a_circle(user_pid, public_id):
    circle = db.session.query(
        Circle.public_id,
        Circle.name,
        Circle.bio,
        Circle.photo,
        Circle.registered_on,
        func.count(circle_member_table.c.circle_pid).filter(circle_member_table.c.is_admin == None).label("member_count")
    ).filter(
        Circle.public_id == public_id
    ).outerjoin(
        circle_member_table
    ).group_by(
        Circle.public_id,
        Circle.name,
        Circle.bio,
        Circle.photo,
        Circle.registered_on
    ).first()

    if circle:
        notification_list = Notification.query.filter_by(
            circle_subject_id=public_id,
            user_recipient_id=user_pid,
            _type=0
        ).all()
        for notif in notification_list:
            notif.is_read = True
        db.session.commit()
        return dict(
            public_id = circle[0],
            name = circle[1],
            bio = circle[2],
            _type = [
                dict(
                    type_pid = _type[0],
                    type_name = _type[1]
                ) for _type in db.session.query(
                    circle_type_table.c.type_pid, 
                    CircleType.name
                    ).filter(circle_type_table.c.circle_pid==circle[0]
                    ).filter(circle_type_table.c.type_pid==CircleType.public_id
                    ).all()
            ],
            photo = circle[3],
            registered_on = circle[4],
            member_count = circle[5],
            visitor_auth = 3 if db.session.query(
                circle_member_table
            ).filter(
                circle_member_table.c.circle_pid == public_id
            ).filter(
                circle_member_table.c.is_admin == True
            ).filter(
                circle_member_table.c.member_pid == user_pid
            ).filter(
                circle_member_table.c.is_accepted == True
            ).first() else 2 if db.session.query(
                circle_member_table
            ).filter(
                circle_member_table.c.circle_pid == public_id
            ).filter(
                circle_member_table.c.member_pid == user_pid
            ).filter(
                circle_member_table.c.is_accepted == True
            ).first() else 1 if db.session.query(
                circle_member_table
            ).filter(
                circle_member_table.c.circle_pid == public_id
            ).filter(
                circle_member_table.c.member_pid == user_pid
            ).filter(
                circle_member_table.c.is_accepted == False
            ).first() else 0,
            admin = [
                dict(
                    admin_id = admin[0],
                    admin_name = admin[1],
                    admin_username = admin[2],
                    admin_photo = admin[3],
                ) for admin in db.session.query(
                    User.public_id,
                    User.name,
                    User.username,
                    User.photo
                ).filter(circle_member_table.c.member_pid==User.public_id
                ).filter(circle_member_table.c.is_admin==True
                ).filter(circle_member_table.c.circle_pid==circle[0]
                ).all()
            ]
        )