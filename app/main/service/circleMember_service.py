import uuid
from sqlalchemy import func

from app.main import db
from app.main.model.circle import Circle
from app.main.model.user import User, circle_member_table
from app.main.service import circle_service, table_save_changes

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

        if not member:
            statement = circle_member_table.insert().values(
                public_id=str(uuid.uuid4()),
                circle_pid=public_id,
                member_pid=user_pid
            )
            table_save_changes(statement)
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

def delete_circle_member(user_pid, public_id, member_id, data):
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
        ).first()

        member_list_length = db.session.query(
            func.count(circle_member_table.c.public_id)
        ).filter(
            circle_member_table.c.circle_pid == public_id
        ).scalar()

        admin_list_length = db.session.query(
            func.count(circle_member_table.c.public_id)
        ).filter(
            circle_member_table.c.circle_pid == public_id
        ).filter(
            circle_member_table.c.is_admin == True
        ).scalar()

        if requestor and target_member:
            admin = db.session.query(
                circle_member_table
            ).filter(
                circle_member_table.c.circle_pid == public_id
            ).filter(
                circle_member_table.c.member_pid == user_pid
            ).filter(
                circle_member_table.c.is_admin == True
            ).first()

            if admin:
                if user_pid == member_id:
                    # ADMIN KICKS HIMSELF
                    if admin_list_length != 1:
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
                    elif member_list_length == 1:
                        statement = circle_member_table.delete().where(
                            circle_member_table.c.member_pid==member_id
                        ).where(
                            circle_member_table.c.circle_pid==public_id
                        )
                        table_save_changes(statement)

                        circle_service.delete_a_circle(public_id, user_pid, data)
                    else:
                        response_object = {
                            'status': 'fail',
                            'message': 'Circle must have another admin before deletion.'
                        }
                        return response_object, 403
                else:
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
                    'message': 'Request unauthorized.'
                }
                return response_object, 401
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
        ).first()

        if admin and member:
            statement = circle_member_table.update().where(
                circle_member_table.c.member_pid==member_id
            ).where(
                circle_member_table.c.circle_pid==public_id
            ).values(
                is_accepted = True
            )
            table_save_changes(statement)
            response_object = {
                'status': 'success',
                'message': 'Circle member successfully accepted.'
            }
            return response_object, 201
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

def get_all_circle_members(public_id, type):
    circle = Circle.query.filter_by(public_id=public_id).first()
    if circle:
        return db.session.query(
            User
        ).filter(
            circle_member_table.c.circle_pid == public_id
        ).filter(
            circle_member_table.c.member_pid == User.public_id
        ).filter(
            circle_member_table.c.is_accepted == (False if type == "0" else True)
        ).all()

    else:
        response_object = {
            'status': 'fail',
            'message': 'No circle found.'
        }
        return response_object, 404