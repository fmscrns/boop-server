from app.main.model.notification import Notification
import uuid
from sqlalchemy import func, or_
from app.main import db
from app.main.model.circle import Circle
from app.main.model.user import User, circle_member_table
from app.main.service import circle_service, notification_service, table_save_changes

def create_circle_member(user_pid, public_id):
    circle = Circle.query.filter_by(public_id=public_id).first()
    if circle:
        member = db.session.query(
            circle_member_table
        ).filter(
            circle_member_table.c.circle_pid == public_id
        ).filter(
            circle_member_table.c.member_pid == user_pid
        ).first()

        admin_list = db.session.query(
            circle_member_table.c.member_pid
        ).filter(
            circle_member_table.c.circle_pid == public_id
        ).filter(
            circle_member_table.c.is_admin == True
        ).all()

        if not member:
            statement = circle_member_table.insert().values(
                public_id=str(uuid.uuid4()),
                circle_pid=public_id,
                member_pid=user_pid
            )
            table_save_changes(statement)

            for admin in admin_list:
                notification_service.save_new_notification(
                    "{} has requested to join {}.".format(
                        User.query.filter_by(public_id=user_pid).first().name,
                        circle.name
                    ),
                    1,
                    user_pid,
                    admin[0],
                    circle_subject_id = circle.public_id
                )

            response_object = {
                'status': 'success',
                'message': 'Wait to be accepted by the admin.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Circle member already exists.',
            }
            return response_object, 409
    else:
        response_object = {
            'status': 'fail',
            'message': 'No circle found.'
        }
        return response_object, 404

def delete_circle_member(user_pid, public_id, member_id):
    circle = Circle.query.filter_by(public_id=public_id).first()
    if circle:
        requestor = db.session.query(
            circle_member_table
        ).filter(
            circle_member_table.c.circle_pid == public_id
        ).filter(
            circle_member_table.c.member_pid == user_pid
        ).first()

        target_member = db.session.query(
            circle_member_table
        ).filter(
            circle_member_table.c.circle_pid == public_id
        ).filter(
            circle_member_table.c.member_pid == member_id
        ).filter(
            circle_member_table.c.is_admin == False
        ).first()

        if requestor and target_member:
            admin_requestor = db.session.query(
                circle_member_table
            ).filter(
                circle_member_table.c.circle_pid == public_id
            ).filter(
                circle_member_table.c.member_pid == user_pid
            ).filter(
                circle_member_table.c.is_admin == True
            ).first()

            if admin_requestor:
                statement = circle_member_table.delete().where(
                    circle_member_table.c.member_pid==member_id
                ).where(
                    circle_member_table.c.circle_pid==public_id
                )
                table_save_changes(statement)
                response_object = {
                    'status': 'success',
                    'message': 'Circle member successfully deleted.'
                }
                return response_object, 201
            elif user_pid == member_id:
                statement = circle_member_table.delete().where(
                    circle_member_table.c.member_pid==member_id
                ).where(
                    circle_member_table.c.circle_pid==public_id
                )
                table_save_changes(statement)
                response_object = {
                    'status': 'success',
                    'message': 'Circle member successfully deleted.'
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Forbidden.'
                }
                return response_object, 403
        else:
            response_object = {
                'status': 'fail',
                'message': 'Circle member does not exist.',
            }
            return response_object, 404
    else:
        response_object = {
            'status': 'fail',
            'message': 'No circle found.'
        }
        return response_object, 404

def accept_circle_member(user_pid, public_id, member_id):
    circle = Circle.query.filter_by(public_id=public_id).first()
    if circle:
        admin = db.session.query(
            circle_member_table
        ).filter(
            circle_member_table.c.circle_pid == public_id
        ).filter(
            circle_member_table.c.member_pid == user_pid
        ).filter(
            circle_member_table.c.is_admin == True
        ).first()

        member = db.session.query(
            circle_member_table
        ).filter(
            circle_member_table.c.circle_pid == public_id
        ).filter(
            circle_member_table.c.member_pid == member_id
        ).filter(
            circle_member_table.c.is_accepted == False
        ).first()

        if admin:
            if member:
                statement = circle_member_table.update().where(
                    circle_member_table.c.member_pid==member_id
                ).where(
                    circle_member_table.c.circle_pid==public_id
                ).values(
                    is_accepted = True
                )
                table_save_changes(statement)

                notification_service.save_new_notification(
                    "{} has accepted your request to join {}.".format(
                        User.query.filter_by(public_id=user_pid).first().name,
                        circle.name
                    ),
                    0,
                    user_pid,
                    member_id,
                    circle_subject_id = circle.public_id
                )

                response_object = {
                    'status': 'success',
                    'message': 'Circle member successfully accepted.'
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Pending member does not exist anymore.',
                }
                return response_object, 404
        else:
            response_object = {
                'status': 'fail',
                'message': 'Request unauthorized.',
            }
            return response_object, 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'No circle found.'
        }
        return response_object, 404

def get_all_circle_members(requestor_pid, public_id, type, search_value):
    circle = Circle.query.filter_by(public_id=public_id).first()
    requesting_admin = db.session.query(
        circle_member_table
    ).filter(
        circle_member_table.c.member_pid == requestor_pid
    ).filter(
        circle_member_table.c.circle_pid == public_id
    ).filter(
        circle_member_table.c.is_admin == True
    ).first()
    if circle:
        if (requesting_admin is not None and type == "0") or (type == "1"):
            if type == "0":
                notification_list = Notification.query.filter_by(
                    circle_subject_id=public_id,
                    user_recipient_id=requestor_pid,
                    _type=1
                ).all()
                for notif in notification_list:
                    notif.is_read = True
                db.session.commit()
            return db.session.query(
                User
            ).filter(
                circle_member_table.c.circle_pid == public_id
            ).filter(
                circle_member_table.c.member_pid == User.public_id
            ).filter(
                circle_member_table.c.is_accepted == (False if type == "0" else True)
            ).filter(
                or_(User.name.ilike("%{}%".format(search_value if search_value else "")),
                User.username.ilike("%{}%".format(search_value if search_value else "")))
            ).filter(
                circle_member_table.c.is_admin == False
            ).all()
        else:
            response_object = {
                'status': 'fail',
                'message': 'Forbidden.'
            }
            return response_object, 403
    else:
        response_object = {
            'status': 'fail',
            'message': 'No circle found.'
        }
        return response_object, 404

def create_circle_admin(user_pid, circle_pid, data):
    circle = Circle.query.filter_by(public_id=circle_pid).first()
    if circle:
        member = db.session.query(
            circle_member_table
        ).filter(
            circle_member_table.c.member_pid == data.get("public_id")
        ).filter(
            circle_member_table.c.circle_pid == circle_pid
        ).filter(
            circle_member_table.c.is_accepted == True
        ).first()

        requesting_admin = db.session.query(
            circle_member_table
        ).filter(
            circle_member_table.c.member_pid == user_pid
        ).filter(
            circle_member_table.c.circle_pid == circle_pid
        ).filter(
            circle_member_table.c.is_admin == True
        ).first()

        if member and requesting_admin:
            member_is_admin = db.session.query(
                circle_member_table
            ).filter(
                circle_member_table.c.member_pid == data.get("public_id")
            ).filter(
                circle_member_table.c.circle_pid == circle_pid
            ).filter(
                circle_member_table.c.is_admin == True
            ).first()

            if not member_is_admin:
                statement = circle_member_table.update().where(
                    circle_member_table.c.member_pid == data.get("public_id")
                ).where(
                    circle_member_table.c.circle_pid == circle_pid
                ).values(
                    is_admin=True
                )
                table_save_changes(statement)

                notification_service.save_new_notification(
                    "{} has made you an admin of {}.".format(
                        User.query.filter_by(public_id=user_pid).first().name,
                        circle.name
                    ),
                    0,
                    user_pid,
                    data.get("public_id"),
                    circle_subject_id = circle_pid
                )

                response_object = {
                    'status': 'success',
                    'message': 'Circle successfully have new admin.'
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User is already an admin of the circle.',
                }
                return response_object, 409
        else:
            response_object = {
                'status': 'fail',
                'message': 'Forbidden.',
            }
            return response_object, 403
    else:
        response_object = {
            'status': 'fail',
            'message': 'No circle found.'
        }
        return response_object, 404

def delete_circle_admin(user_pid, circle_pid, admin_id, data):
    circle = Circle.query.filter_by(public_id=circle_pid).first()
    if circle:
        requestor = db.session.query(
            circle_member_table
        ).filter(
            circle_member_table.c.member_pid == user_pid
        ).filter(
            circle_member_table.c.circle_pid == circle_pid
        ).filter(
            circle_member_table.c.is_admin == True
        ).first()

        target_admin = db.session.query(
            circle_member_table
        ).filter(
            circle_member_table.c.member_pid == admin_id
        ).filter(
            circle_member_table.c.circle_pid == circle_pid
        ).filter(
            circle_member_table.c.is_admin == True
        ).first()

        admin_list_length = db.session.query(
            func.count(circle_member_table.c.public_id)
        ).filter(
            circle_member_table.c.circle_pid == circle_pid
        ).filter(
            circle_member_table.c.is_admin == True
        ).scalar()
        if requestor and target_admin:
            if admin_list_length != 1:
                statement = circle_member_table.update().where(
                    circle_member_table.c.member_pid==admin_id
                ).where(
                    circle_member_table.c.circle_pid==circle_pid
                ).values(
                    is_admin = False
                )
                table_save_changes(statement)

                notification_service.save_new_notification(
                    "{} has removed you as admin of {}.".format(
                        User.query.filter_by(public_id=user_pid).first().name,
                        circle.name
                    ),
                    0,
                    user_pid,
                    admin_id,
                    circle_subject_id = circle_pid
                )

                response_object = {
                    'status': 'success',
                    'message': 'Circle admin successfully removed.'
                }
                return response_object, 201
            else:
                return circle_service.delete_a_circle(circle_pid, user_pid, data)
        else:
            response_object = {
                'status': 'fail',
                'message': 'Forbidden.',
            }
            return response_object, 403
    else:
        response_object = {
            'status': 'fail',
            'message': 'No pet found.'
        }
        return response_object, 404