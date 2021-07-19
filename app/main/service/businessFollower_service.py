from app.main.model.notification import Notification
import uuid
from sqlalchemy import func
from app.main import db
from app.main.model.business import Business
from app.main.model.user import User, business_follower_table
from app.main.service import notification_service, table_save_changes
from app.main.service import business_service

def create_business_follower(requestor_pid, business_pid):
    business = Business.query.filter_by(public_id=business_pid).first()
    if business:
        follower = db.session.query(
            business_follower_table
        ).filter(
            business_follower_table.c.business_pid == business_pid
        ).filter(
            business_follower_table.c.follower_pid == requestor_pid
        ).first()

        exec_list = db.session.query(
            business_follower_table.c.follower_pid
        ).filter(
            business_follower_table.c.business_pid == business_pid
        ).filter(
            business_follower_table.c.is_executive == True
        ).all()

        if not follower:
            statement = business_follower_table.insert().values(
                public_id=str(uuid.uuid4()),
                business_pid=business_pid,
                follower_pid=requestor_pid
            )
            table_save_changes(statement)

            for exec in exec_list:
                notification_service.save_new_notification(
                    "{} followed {}".format(
                        User.query.filter_by(public_id=requestor_pid).first().name,
                        business.name
                    ),
                    0,
                    requestor_pid,
                    exec[0],
                    business_subject_id = business.public_id
                )
            
            response_object = {
                'status': 'success',
                'message': 'Business successfully followed.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Business already followed.',
            }
            return response_object, 409
    else:
        response_object = {
            'status': 'fail',
            'message': 'No business found.'
        }
        return response_object, 404

def delete_business_follower(requestor_pid, business_pid, follower_pid):
    business = Business.query.filter_by(public_id=business_pid).first()
    if business:
        requestor = db.session.query(
            business_follower_table
        ).filter(
            business_follower_table.c.business_pid == business_pid
        ).filter(
            business_follower_table.c.follower_pid == requestor_pid
        ).first()

        target_follower = db.session.query(
            business_follower_table
        ).filter(
            business_follower_table.c.business_pid == business_pid
        ).filter(
            business_follower_table.c.follower_pid == follower_pid
        ).filter(
            business_follower_table.c.is_executive == False
        ).first()

        if requestor and target_follower:
            admin_requestor = db.session.query(
                business_follower_table
            ).filter(
                business_follower_table.c.business_pid == business_pid
            ).filter(
                business_follower_table.c.follower_pid == requestor_pid
            ).filter(
                business_follower_table.c.is_executive == True
            ).first()

            if admin_requestor:
                statement = business_follower_table.delete().where(
                    business_follower_table.c.follower_pid==follower_pid
                ).where(
                    business_follower_table.c.business_pid==business_pid
                )
                table_save_changes(statement)
                response_object = {
                    'status': 'success',
                    'message': 'Business follower successfully deleted.'
                }
                return response_object, 201
            elif requestor_pid == follower_pid:
                statement = business_follower_table.delete().where(
                    business_follower_table.c.follower_pid==follower_pid
                ).where(
                    business_follower_table.c.business_pid==business_pid
                )
                table_save_changes(statement)
                response_object = {
                    'status': 'success',
                    'message': 'Business follower successfully deleted.'
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
                'message': 'Business follower does not exist.',
            }
            return response_object, 404
    else:
        response_object = {
            'status': 'fail',
            'message': 'No business found.'
        }
        return response_object, 404 

def get_all_business_followers(requestor_pid, business_pid):
    business = business_service.get_a_business(requestor_pid, business_pid)
    if business:
        if business["visitor_auth"] == 2:
            notification_list = Notification.query.filter_by(
                business_subject_id=business["public_id"],
                user_recipient_id=requestor_pid,
                _type=1
            ).all()
            for notif in notification_list:
                notif.is_read = True
            db.session.commit()
        return db.session.query(
            User
        ).filter(
            business_follower_table.c.business_pid == business_pid
        ).filter(
            business_follower_table.c.follower_pid == User.public_id
        ).filter(
            business_follower_table.c.is_executive == False
        ).all()

    else:
        response_object = {
            'status': 'fail',
            'message': 'No business found.'
        }
        return response_object, 404

def create_business_executive(requestor_pid, business_pid, data):
    business = Business.query.filter_by(public_id=business_pid).first()
    if business:
        user = User.query.filter_by(public_id=data.get("public_id")).first()
        admin = db.session.query(
            business_follower_table
        ).filter(
            business_follower_table.c.follower_pid == requestor_pid
        ).filter(
            business_follower_table.c.business_pid == business_pid
        ).filter(
            business_follower_table.c.is_executive == True
        ).first()

        if user and admin:
            follower = db.session.query(
                business_follower_table
            ).filter(
                business_follower_table.c.follower_pid == data.get("public_id")
            ).filter(
                business_follower_table.c.business_pid == business_pid
            ).first()

            if follower:
                if follower[4] == False:
                    statement = business_follower_table.update().where(
                        business_follower_table.c.follower_pid==data.get("public_id")
                    ).where(
                        business_follower_table.c.business_pid==business_pid
                    ).values(
                        is_executive = True,
                    )
                    table_save_changes(statement)

                    notification_service.save_new_notification(
                        "{} has made you an executive of {}.".format(
                            User.query.filter_by(public_id=requestor_pid).first().name,
                            business.name
                        ),
                        0,
                        requestor_pid,
                        data.get("public_id"),
                        business_subject_id = business_pid
                    )

                    response_object = {
                        'status': 'success',
                        'message': 'Business successfully have new executive.'
                    }
                    return response_object, 201
                else:
                    response_object = {
                        'status': 'fail',
                        'message': 'User is already an executive of the business.',
                    }
                    return response_object, 409
            else:
                statement = business_follower_table.insert().values(
                    public_id=str(uuid.uuid4()),
                    follower_pid=data.get("public_id"),
                    business_pid=business_pid,
                    is_executive=True
                )
                table_save_changes(statement)
                notification_service.save_new_notification(
                    "{} has made you an executive of {}.".format(
                        User.query.filter_by(public_id=requestor_pid).first().name,
                        business.name
                    ),
                    0,
                    requestor_pid,
                    data.get("public_id"),
                    business_subject_id = business_pid
                )
                response_object = {
                    'status': 'success',
                    'message': 'Business successfully have new executive.'
                }
                return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Forbidden.',
            }
            return response_object, 403
    else:
        response_object = {
            'status': 'fail',
            'message': 'No business found.'
        }
        return response_object, 404

def delete_business_executive(requestor_pid, business_pid, executive_pid, data):
    business = Business.query.filter_by(public_id=business_pid).first()
    if business:
        requestor = db.session.query(
            business_follower_table
        ).filter(
            business_follower_table.c.follower_pid == requestor_pid
        ).filter(
            business_follower_table.c.business_pid == business_pid
        ).filter(
            business_follower_table.c.is_executive == True
        ).first()

        target_admin = db.session.query(
            business_follower_table
        ).filter(
            business_follower_table.c.follower_pid == executive_pid
        ).filter(
            business_follower_table.c.business_pid == business_pid
        ).filter(
            business_follower_table.c.is_executive == True
        ).first()

        admin_list_length = db.session.query(
            func.count(business_follower_table.c.public_id)
        ).filter(
            business_follower_table.c.business_pid == business_pid
        ).filter(
            business_follower_table.c.is_executive == True
        ).scalar()
        if requestor and target_admin:
            if admin_list_length != 1:
                statement = business_follower_table.update().where(
                    business_follower_table.c.follower_pid==executive_pid
                ).where(
                    business_follower_table.c.business_pid==business_pid
                ).values(
                    is_executive = False
                )
                table_save_changes(statement)

                notification_service.save_new_notification(
                    "{} has removed you as executive of {}.".format(
                        User.query.filter_by(public_id=requestor_pid).first().name,
                        business.name
                    ),
                    0,
                    requestor_pid,
                    executive_pid,
                    business_subject_id = business_pid
                )

                response_object = {
                    'status': 'success',
                    'message': 'Business executive successfully removed.'
                }
                return response_object, 201
            else:
                return business_service.delete_a_business(business_pid, requestor_pid, data)
        else:
            response_object = {
                'status': 'fail',
                'message': 'Forbidden.',
            }
            return response_object, 403
    else:
        response_object = {
            'status': 'fail',
            'message': 'No business found.'
        }
        return response_object, 404