from sqlalchemy.sql.expression import outerjoin
from sqlalchemy.sql.functions import func
from app.main.model.specie import Specie
from app.main.model.preference import Preference
from app.main.model.breed import Breed
from app.main.model.circle_type import CircleType
from app.main.model.business_type import BusinessType
import uuid
from app.main import db
from . import model_save_changes

def save_new_preferences(user_pid, data):
    if data.get("breed_subgroup"):
        pref_list = Preference.query.filter_by(user_selector_id=user_pid).filter(Preference.breed_subgroup_id != None).all()
        for item in data.get("breed_subgroup"):
            breed = Breed.query.filter_by(public_id=item["public_id"]).first()
            if breed:
                new_preference = Preference(
                    public_id = str(uuid.uuid4()),
                    user_selector_id = user_pid
                )
                new_preference.breed_subgroup_id = item["public_id"]
                model_save_changes(new_preference)
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'No breed found.'
                }
                return response_object, 404
        for a in pref_list:
            db.session.delete(a)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Preference successfully registered.'
        }
        return response_object, 201

    if data.get("business_type"):
        pref_list = Preference.query.filter_by(user_selector_id=user_pid).filter(Preference.business_type_id != None).all()
        for item in data.get("business_type"):
            business_type = BusinessType.query.filter_by(public_id=item["public_id"]).first()
            if business_type:
                new_preference = Preference(
                    public_id = str(uuid.uuid4()),
                    user_selector_id = user_pid
                )
                new_preference.business_type_id = item["public_id"]
                model_save_changes(new_preference)
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'No business type found.'
                }
                return response_object, 404
        for a in pref_list:
            db.session.delete(a)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Preference successfully registered.'
        }
        return response_object, 201

    if data.get("circle_type"):
        pref_list = Preference.query.filter_by(user_selector_id=user_pid).filter(Preference.circle_type_id != None).all()
        for item in data.get("circle_type"):
            circle_type = CircleType.query.filter_by(public_id=item["public_id"]).first()
            if circle_type:
                new_preference = Preference(
                    public_id = str(uuid.uuid4()),
                    user_selector_id = user_pid
                )
                new_preference.circle_type_id = item["public_id"]
                model_save_changes(new_preference)
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'No circle type found.'
                }
                return response_object, 404
        for a in pref_list:
            db.session.delete(a)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Preference successfully registered.'
        }
        return response_object, 201