# app/__init__.py

from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.specie_controller import api as specie_ns
from .main.controller.breed_controller import api as breed_ns
from .main.controller.pet_controller import api as pet_ns
from .main.controller.business_controller import api as business_ns
from .main.controller.post_controller import api as post_ns
from .main.controller.businessType_controller import api as businessType_ns
from .main.controller.circleType_controller import api as circleType_ns
from .main.controller.circle_controller import api as circle_ns
from .main.controller.comment_controller import api as comment_ns
from .main.controller.notification_controller import api as notification_ns
from .main.controller.preference_controller import api as preference_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(specie_ns, path='/specie')
api.add_namespace(breed_ns, path='/breed')
api.add_namespace(pet_ns, path='/pet')
api.add_namespace(business_ns, path='/business')
api.add_namespace(post_ns, path='/post')
api.add_namespace(businessType_ns, path='/business_type')
api.add_namespace(circle_ns, path='/circle')
api.add_namespace(circleType_ns, path='/circle_type')
api.add_namespace(comment_ns, path='/comment')
api.add_namespace(notification_ns, path="/notification")
api.add_namespace(preference_ns, path="/preference")

populate_bp = Blueprint("populate", __name__)

from app.main import db
from app.main.model.user import User, pet_follower_table, business_follower_table, circle_member_table, post_liker_table
from app.main.model.specie import Specie
from app.main.model.breed import Breed
from app.main.model.business_type import BusinessType
from app.main.model.circle_type import CircleType
from app.main.model.pet import Pet, post_subject_table
from app.main.model.business import Business
from app.main.model.business_operation import BusinessOperation
from app.main.model.circle import Circle
from app.main.model.post import Post
from app.main.model.comment import Comment
from app.main.model.preference import Preference

import pandas as pd
import os

@populate_bp.route("/user", methods=["GET"])
def users():
    try:
        dataframe = pd.read_excel(
            os.path.dirname(os.path.abspath(__file__)) + "/boop-populate.xlsx",
            sheet_name="User",
            header=0
        )

        for index, row in dataframe.iterrows():
            statement = User(
                public_id = row["public_id"],
                name=row["name"],
                email=row['email'],
                username=row['username'],
                password=row['password'],
                registered_on=row["registered_on"],
                admin=row["admin"],
                photo=row["photo"]
            )
            db.session.add(statement)
            db.session.commit()

        return "DONE"
        
    except Exception as e:
        return str(e)
        
@populate_bp.route("/species", methods=["GET"])
def species():
    try:
        dataframe = pd.read_excel(
            os.path.dirname(os.path.abspath(__file__)) + "/boop-populate.xlsx",
            sheet_name="Species",
            header=0
        )
        
        for index, row in dataframe.iterrows():
            statement = Specie(
                public_id=row["public_id"],
                name=row["name"],
                registered_on=row["registered_on"]
            )
            db.session.add(statement)
            db.session.commit()

        return "DONE"

    except Exception as e:
        return str(e)

@populate_bp.route("/breed", methods=["GET"])
def breed():
    try:
        dataframe = pd.read_excel(
            os.path.dirname(os.path.abspath(__file__)) + "/boop-populate.xlsx",
            sheet_name="Breed",
            header=0
        )
        
        for index, row in dataframe.iterrows():
            statement = Breed(
                public_id=row["public_id"],
                name=row["name"],
                specie_parent_id=row["specie_parent_id"],
                registered_on=row["registered_on"]
            )
            db.session.add(statement)
            db.session.commit()

        return "DONE"

    except Exception as e:
        return str(e)

@populate_bp.route("/business_type", methods=["GET"])
def business_type():
    try:
        dataframe = pd.read_excel(
            os.path.dirname(os.path.abspath(__file__)) + "/boop-populate.xlsx",
            sheet_name="Business Type",
            header=0
        )
        
        for index, row in dataframe.iterrows():
            statement = BusinessType(
                public_id=row["public_id"],
                name=row["name"],
                registered_on=row["registered_on"]
            )
            db.session.add(statement)
            db.session.commit()

        return "DONE"

    except Exception as e:
        return str(e)

@populate_bp.route("/circle_type", methods=["GET"])
def circle_type():
    try:
        dataframe = pd.read_excel(
            os.path.dirname(os.path.abspath(__file__)) + "/boop-populate.xlsx",
            sheet_name="Circle Type",
            header=0
        )
        
        for index, row in dataframe.iterrows():
            statement = CircleType(
                public_id=row["public_id"],
                name=row["name"],
                registered_on=row["registered_on"]
            )
            db.session.add(statement)
            db.session.commit()

        return "DONE"

    except Exception as e:
        return str(e)

@populate_bp.route("/pet", methods=["GET"])
def pet():
    try:
        dataframe = pd.read_excel(
            os.path.dirname(os.path.abspath(__file__)) + "/boop-populate.xlsx",
            sheet_name="Pet",
            header=0
        )
        
        for index, row in dataframe.iterrows():
            statement = Pet(
                public_id = row["public_id"],
                name = row["name"],
                bio = row["bio"],
                birthday = row["birthday"],
                sex = row["sex"],
                status = row["status"],
                is_private = row["is_private"],
                photo = row["photo"],
                registered_on = row["registered_on"],
                specie_group_id = row["specie_group_id"],
                breed_subgroup_id = row["breed_subgroup_id"]
            )
            db.session.add(statement)
            db.session.commit()

        return "DONE"

    except Exception as e:
        return str(e)

@populate_bp.route("/pet_follower", methods=["GET"])
def pet_follower():
    try:
        dataframe = pd.read_excel(
            os.path.dirname(os.path.abspath(__file__)) + "/boop-populate.xlsx",
            sheet_name="Pet Follower",
            header=0
        )
        
        for index, row in dataframe.iterrows():
            statement = pet_follower_table.insert().values(
                public_id = row["public_id"],
                follower_pid=row["follower_pid"],
                is_owner=row["is_owner"],
                pet_pid=row["pet_pid"],
                is_accepted=row["is_accepted"]
            )
            db.session.execute(statement)
            db.session.commit()

        return "DONE"

    except Exception as e:
        return str(e)

@populate_bp.route("/business", methods=["GET"])
def business():
    try:
        dataframe = pd.read_excel(
            os.path.dirname(os.path.abspath(__file__)) + "/boop-populate.xlsx",
            sheet_name="Business",
            header=0
        )
        
        for index, row in dataframe.iterrows():
            statement = Business(
                public_id = row["public_id"],
                name = row["name"],
                bio = row["bio"],
                photo = row["photo"],
                registered_on = row["registered_on"]
            )
            db.session.add(statement)
            db.session.commit()

        return "DONE"

    except Exception as e:
        return str(e)

@populate_bp.route("/business_follower", methods=["GET"])
def business_follower():
    try:
        dataframe = pd.read_excel(
            os.path.dirname(os.path.abspath(__file__)) + "/boop-populate.xlsx",
            sheet_name="Business Follower",
            header=0
        )
        
        for index, row in dataframe.iterrows():
            statement = business_follower_table.insert().values(
                public_id = row["public_id"],
                business_pid=row["business_pid"],
                follower_pid=row["follower_pid"],
                is_executive=row["is_executive"],
                registered_on=row["registered_on"]
            )
            db.session.execute(statement)
            db.session.commit()

        return "DONE"

    except Exception as e:
        return str(e)

@populate_bp.route("/business_operation", methods=["GET"])
def business_operation():
    try:
        dataframe = pd.read_excel(
            os.path.dirname(os.path.abspath(__file__)) + "/boop-populate.xlsx",
            sheet_name="Business Operation",
            header=0
        )
        
        for index, row in dataframe.iterrows():
            statement = BusinessOperation(
                public_id = row["public_id"],
                day = row["day"],
                is_open = row["is_open"],
                start_at = row["start_at"],
                end_at = row["end_at"],
                business_prop_id = row["business_prop_id"]
            )
            db.session.add(statement)
            db.session.commit()

        return "DONE"

    except Exception as e:
        return str(e)

@populate_bp.route("/circle", methods=["GET"])
def circle():
    try:
        dataframe = pd.read_excel(
            os.path.dirname(os.path.abspath(__file__)) + "/boop-populate.xlsx",
            sheet_name="Circle",
            header=0
        )
        
        for index, row in dataframe.iterrows():
            statement = Circle(
                public_id = row["public_id"],
                name = row["name"],
                bio = row["bio"],
                photo = row["photo"],
                registered_on = row["registered_on"]
            )
            db.session.add(statement)
            db.session.commit()

        return "DONE"

    except Exception as e:
        return str(e)

@populate_bp.route("/circle_member", methods=["GET"])
def circle_member():
    try:
        dataframe = pd.read_excel(
            os.path.dirname(os.path.abspath(__file__)) + "/boop-populate.xlsx",
            sheet_name="Circle Member",
            header=0
        )
        
        for index, row in dataframe.iterrows():
            statement = circle_member_table.insert().values(
                public_id = row["public_id"],
                circle_pid=row["circle_pid"],
                member_pid=row["member_pid"],
                is_accepted=row["is_accepted"],
                is_admin=row["is_admin"],
                registered_on=row["registered_on"]
            )
            db.session.execute(statement)
            db.session.commit()

        return "DONE"

    except Exception as e:
        return str(e)

@populate_bp.route("/post", methods=["GET"])
def post():
    try:
        dataframe = pd.read_excel(
            os.path.dirname(os.path.abspath(__file__)) + "/boop-populate.xlsx",
            sheet_name="Post",
            header=0
        )
        
        for index, row in dataframe.iterrows():
            statement = Post(
                public_id = row["public_id"],
                content = row["content"],
                photo_1 = row["photo_1"] if isinstance(row["photo_1"], str) else None,
                photo_2 = row["photo_2"] if isinstance(row["photo_2"], str) else None,
                photo_3 = row["photo_3"] if isinstance(row["photo_3"], str) else None,
                photo_4 = row["photo_4"] if isinstance(row["photo_4"], str) else None,
                registered_on = row["registered_on"],
                user_creator_id = row["user_creator_id"],
                business_pinboard_id=row["business_pinboard_id"] if isinstance(row["business_pinboard_id"], str) else None,
                circle_confiner_id=row["circle_confiner_id"] if isinstance(row["circle_confiner_id"], str) else None
            )
            db.session.add(statement)
            db.session.commit()

        return "DONE"

    except Exception as e:
        return str(e)

@populate_bp.route("/post_subject", methods=["GET"])
def post_subject():
    try:
        dataframe = pd.read_excel(
            os.path.dirname(os.path.abspath(__file__)) + "/boop-populate.xlsx",
            sheet_name="Post Subject",
            header=0
        )
        
        for index, row in dataframe.iterrows():
            statement = post_subject_table.insert().values(
                public_id = row["public_id"],
                post_pid = row["post_pid"],
                subject_pid = row["subject_pid"],
                registered_on=row["registered_on"]
            )
            db.session.execute(statement)
            db.session.commit()

        return "DONE"

    except Exception as e:
        return str(e)

@populate_bp.route("/post_liker", methods=["GET"])
def post_liker():
    try:
        dataframe = pd.read_excel(
            os.path.dirname(os.path.abspath(__file__)) + "/boop-populate.xlsx",
            sheet_name="Post Liker",
            header=0
        )
        
        for index, row in dataframe.iterrows():
            statement = post_liker_table.insert().values(
                public_id = row["public_id"],
                post_pid=row["post_pid"],
                liker_pid=row["liker_pid"],
                is_unliked=row["is_unliked"],
                registered_on=row["registered_on"]
            )
            db.session.execute(statement)
            db.session.commit()

        return "DONE"

    except Exception as e:
        return str(e)

@populate_bp.route("/comment", methods=["GET"])
def comment():
    try:
        dataframe = pd.read_excel(
            os.path.dirname(os.path.abspath(__file__)) + "/boop-populate.xlsx",
            sheet_name="Comment",
            header=0
        )
        
        for index, row in dataframe.iterrows():
            statement = Comment(
                public_id = row["public_id"],
                content = row["content"],
                photo = row["photo"],
                registered_on = row["registered_on"],
                user_creator_id = row["user_creator_id"],
                post_parent_id = row["post_parent_id"]
            )    
            db.session.add(statement)
            db.session.commit()

        return "DONE"

    except Exception as e:
        return str(e)