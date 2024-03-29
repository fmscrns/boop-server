import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key
from .. import db, flask_bcrypt

circle_member_table = db.Table('circle_member_table',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('public_id', db.String(100), unique=True),
    db.Column('circle_pid', db.String(100), db.ForeignKey('circle.public_id')),
    db.Column('member_pid', db.String(100), db.ForeignKey('user.public_id')),
    db.Column('is_accepted', db.Boolean, default=False),
    db.Column('is_admin', db.Boolean, default=False),
    db.Column('registered_on', db.DateTime, nullable=False, default=datetime.datetime.utcnow)
)

pet_follower_table = db.Table('pet_follower_table',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('public_id', db.String(100), unique=True),
    db.Column('pet_pid', db.String(100), db.ForeignKey('pet.public_id')),
    db.Column('follower_pid', db.String(100), db.ForeignKey('user.public_id')),
    db.Column('is_owner', db.Boolean, default=False),
    db.Column('is_accepted', db.Boolean, default=False),
    db.Column('registered_on', db.DateTime, nullable=False, default=datetime.datetime.utcnow)
)

business_follower_table = db.Table('business_follower_table',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('public_id', db.String(100), unique=True),
    db.Column('business_pid', db.String(100), db.ForeignKey('business.public_id')),
    db.Column('follower_pid', db.String(100), db.ForeignKey('user.public_id')),
    db.Column('is_executive', db.Boolean, default=False),
    db.Column('registered_on', db.DateTime, nullable=False, default=datetime.datetime.utcnow)
)

post_liker_table = db.Table('post_liker_table',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('public_id', db.String(100), unique=True),
    db.Column('post_pid', db.String(100), db.ForeignKey('post.public_id')),
    db.Column('liker_pid', db.String(100), db.ForeignKey('user.public_id')),
    db.Column('is_unliked', db.Boolean, default=False),
    db.Column('registered_on', db.DateTime, nullable=False, default=datetime.datetime.utcnow)
)

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    photo = db.Column(db.String(50), default="default_user.jpg")
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password): 
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod  
    def decode_auth_token(auth_token):
            """
            Decodes the auth token
            :param auth_token:
            :return: integer|string
            """
            try:
                payload = jwt.decode(auth_token, key)
                is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
                if is_blacklisted_token:
                    return 'Token blacklisted. Please log in again.'
                else:
                    return payload['sub']
            except jwt.ExpiredSignatureError:
                return 'Signature expired. Please log in again.'
            except jwt.InvalidTokenError:
                return 'Invalid token. Please log in again.'