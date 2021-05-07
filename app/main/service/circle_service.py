import uuid
import datetime

from app.main import db
from app.main.model.circle import Circle, circle_type_table
from app.main.model.circle_type import CircleType
from app.main.model.user import User

def save_new_circle(user_pid, data):
    try:
        circle_pid = str(uuid.uuid4())
        new_circle = Circle(
            public_id = circle_pid,
            name = data.get("name"),
            bio = data.get("bio"),
            photo = data.get("photo"),
            registered_on = datetime.datetime.utcnow(),
            user_admin_id = user_pid
        )
        save_changes(new_circle)
        for _type in data.get("_type"):
            statement = circle_type_table.insert().values(
                public_id = str(uuid.uuid4()),
                circle_pid = circle_pid,
                type_pid = _type["public_id"]
            )
            db.session.execute(statement)
            db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Circle successfully registered.',
            'payload': User.query.filter_by(public_id=user_pid).first().username
        }
        return response_object, 201
    except:
        return 500

def get_all_circles_by_user(user_pid):
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
            admin_id = circle[5],
            admin_name = circle[6],
            admin_username = circle[7],
            admin_photo = circle[8]
        ) for circle in db.session.query(
            Circle.public_id,
            Circle.name,
            Circle.bio,
            Circle.photo,
            Circle.registered_on,
            User.public_id,
            User.name,
            User.username,
            User.photo
        ).filter(
            Circle.user_admin_id == user_pid
        ).filter(
            Circle.user_admin_id == User.public_id
        ).order_by(Circle.registered_on.desc()).all()
    ]

def patch_a_circle(public_id, user_pid, data):
    circle = Circle.query.filter_by(public_id=public_id).first()

    if circle:
        if circle.user_admin_id == user_pid:
            statement = circle_type_table.delete().where(
                circle_type_table.c.circle_pid==circle.public_id)
            db.session.execute(statement)
            db.session.commit()
            for _type in data.get("_type"):
                statement = circle_type_table.insert().values(
                    public_id = str(uuid.uuid4()),
                    circle_pid = circle.public_id,
                    type_pid = _type["public_id"]
                )
                db.session.execute(statement)
                db.session.commit()
            circle.name = data.get("name")
            circle.bio = data.get("bio")
            circle.photo = data.get("photo")
            db.session.commit()
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
    if circle:
        if circle.user_admin_id == user_pid and data.get("name") == circle.name:
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
            return response_object, 400
    else:
        response_object = {
            'status': 'fail',
            'message': 'No circle found.'
        }
        return response_object, 404

def get_all_circles():
    return Circle.query.all()

def get_a_circle(public_id):
    circle = db.session.query(
        Circle.public_id,
        Circle.name,
        Circle.bio,
        Circle.photo,
        Circle.registered_on,
        User.public_id,
        User.name,
        User.username,
        User.photo
    ).filter(
        Circle.public_id == public_id
    ).filter(
        Circle.user_admin_id == User.public_id
    ).first()

    if circle:
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
            admin_id = circle[5],
            admin_name = circle[6],
            admin_username = circle[7],
            admin_photo = circle[8]
        )

def save_changes(data):
    db.session.add(data)
    db.session.commit()