import uuid
import datetime

from app.main import db
from app.main.model.business import Business, business_type_table
from app.main.model.business_operation import BusinessOperation
from app.main.model.business_type import BusinessType
from app.main.model.user import User
from app.main.service import model_save_changes, table_save_changes

def save_new_business(user_pid, data):
    try:
        business_pid = str(uuid.uuid4())
        new_business = Business(
            public_id = business_pid,
            name = data.get("name"),
            bio = data.get("bio"),
            photo = data.get("photo"),
            registered_on = datetime.datetime.utcnow(),
            user_executive_id = user_pid
        )
        model_save_changes(new_business)
        for _type in data.get("_type"):
            statement = business_type_table.insert().values(
                public_id = str(uuid.uuid4()),
                business_pid = business_pid,
                type_pid = _type["public_id"]
            )
            table_save_changes(statement)
        per_day_data = [
            ["Monday", data.get("mon_open_bool"), data.get("mon_open_time"), data.get("mon_close_time")],
            ["Tuesday", data.get("tue_open_bool"), data.get("tue_open_time"), data.get("tue_close_time")],
            ["Wednesday", data.get("wed_open_bool"), data.get("wed_open_time"), data.get("wed_close_time")],
            ["Thursday", data.get("thu_open_bool"), data.get("thu_open_time"), data.get("thu_close_time")],
            ["Friday", data.get("fri_open_bool"), data.get("fri_open_time"), data.get("fri_close_time")],
            ["Saturday", data.get("sat_open_bool"), data.get("sat_open_time"), data.get("sat_close_time")],
            ["Sunday", data.get("sun_open_bool"), data.get("sun_open_time"), data.get("sun_close_time")],
        ]
        for data in per_day_data:
            new_operation = BusinessOperation(
                public_id = str(uuid.uuid4()),
                day = data[0],
                is_open = data[1],
                start_at = data[2],
                end_at = data[3],
                business_prop_id = business_pid
            )
            model_save_changes(new_operation)
        response_object = {
            'status': 'success',
            'message': 'Business successfully registered.',
            'payload': User.query.filter_by(public_id=user_pid).first().username
        }
        return response_object, 201
    except:
        return 500

def get_all_businesses_by_user(requestor_pid, user_pid):
    if requestor_pid == user_pid:
        return [
            dict(
                public_id = business[0],
                name = business[1],
                bio = business[2],
                _type = [
                    dict(
                        type_pid = _type[0],
                        type_name = _type[1]
                    ) for _type in db.session.query(
                        business_type_table.c.type_pid, 
                        BusinessType.name
                        ).filter(business_type_table.c.business_pid==business[0]
                        ).filter(business_type_table.c.type_pid==BusinessType.public_id
                        ).all()
                ],
                photo = business[3],
                registered_on = business[4],
                executive_id = business[5],
                executive_name = business[6],
                executive_username = business[7],
                executive_photo = business[8]
            ) for business in db.session.query(
                Business.public_id,
                Business.name,
                Business.bio,
                Business.photo,
                Business.registered_on,
                User.public_id,
                User.name,
                User.username,
                User.photo
            ).filter(
                Business.user_executive_id == user_pid
            ).filter(
                Business.user_executive_id == User.public_id
            ).order_by(Business.registered_on.desc()).all()
        ]
    else:
        response_object = {
            'status': 'fail',
            'message': 'Forbidden.'
        }
        return response_object, 403

def patch_a_business(public_id, user_pid, data):
    business = Business.query.filter_by(public_id=public_id).first()

    if business:
        if business.user_executive_id == user_pid:
            statement = business_type_table.delete().where(business_type_table.c.business_pid==business.public_id)
            table_save_changes(statement)
            for _type in data.get("_type"):
                statement = business_type_table.insert().values(
                    public_id = str(uuid.uuid4()),
                    business_pid = business.public_id,
                    type_pid = _type["public_id"]
                )
                table_save_changes(statement)
            business.name = data.get("name")
            business.bio = data.get("bio")
            business.photo = data.get("photo")
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Business successfully updated.'
            }
            return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'No business found.'
        }
        return response_object, 404

def delete_a_business(public_id, user_pid, data):
    business = Business.query.filter_by(public_id=public_id).first()
    if business:
        if business.user_executive_id == user_pid and data.get("name") == business.name:
            db.session.delete(business)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Business successfully deleted.'
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
            'message': 'No business found.'
        }
        return response_object, 404

def get_all_businesses():
    return Business.query.all()

def get_a_business(public_id):
    business = db.session.query(
        Business.public_id,
        Business.name,
        Business.bio,
        Business.photo,
        Business.registered_on,
        User.public_id,
        User.name,
        User.username,
        User.photo
    ).filter(
        Business.public_id == public_id
    ).filter(
        Business.user_executive_id == User.public_id
    ).first()

    if business:
        return dict(
            public_id = business[0],
            name = business[1],
            bio = business[2],
            _type = [
                dict(
                    type_pid = _type[0],
                    type_name = _type[1]
                ) for _type in db.session.query(business_type_table.c.type_pid, BusinessType.name).filter(business_type_table.c.business_pid==business[0]).filter(business_type_table.c.type_pid==BusinessType.public_id).all()
            ],
            photo = business[3],
            registered_on = business[4],
            executive_id = business[5],
            executive_name = business[6],
            executive_username = business[7],
            executive_photo = business[8]
        )