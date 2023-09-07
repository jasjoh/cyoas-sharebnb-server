
from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User in the system."""

    __tablename__ = "users"

    username = db.Column(
        db.Text,
        primary_key=True,
    )

    password = db.Column(
        db.Text,
        nullable=False
    )

    first_name = db.Column(
        db.Text,
        nullable=False
    )

    last_name = db.Column(
        db.Text,
        nullable=False
    )

    properties = db.relationship(
        'Property',
        backref='host_username'
    )

    messages_sent = db.relationship(
        'Message',
        backref='sender'
    )

    messages_received = db.relationship(
        'Message',
        backref='recipient'
    )

    bookings = db.relationship(
        'Bookings',
        backref='booker'
    )

    #class methods for signup and authenticate

    @classmethod
    def signup(cls, username, password, first_name, last_name):
        """Sign up user.

        Hashes password and adds user to session.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        user = cls.query.filter_by(username=username).one_or_none()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Property(db.Model):
    """A listed property."""

    __tablename__ = 'properties'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.Text,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    price_per_day_cents = db.Column(
        db.Integer,
        nullable=False
    )

    host_username = db.Column(
        db.Text,
        db.ForeignKey('users.username')
    )

    photos = db.relationship(
        'Photo',
        backref='property'
    )

    messages = db.relationship(
        'Message',
        backref='property'
    )

    bookings = db.relationship(
        'Booking',
        backref='property'
    )

class Photo(db.Model):
    """A photo of a property."""

    __tablename__ = 'photos'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.Text,
        nullable=False
    )

    property = db.Column(
        db.Integer,
        db.ForeignKey('properties.id')
    )

    url = db.Column(
        db.String,
        nullable=False
    )


class Message(db.Model):
    """A message sent between one user to another."""

    __tablename__ = 'messages'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    text = db.Column(
       db.Text,
       nullable=False
    )

    sender = db.Column(
        db.Text,
        db.ForeignKey('users.username')
    )

    recipient = db.Column(
        db.Text,
        db.ForeignKey('users.username')
    )

    property = db.Column(
        db.Integer,
        db.ForeignKey('properties.id')
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )


class Booking(db.Model):
    """A booking for a property."""

    __tablename__ = 'bookings'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    start_date = db.Column(
        db.Text,
        nullable=False
    )

    end_date = db.Column(
        db.Text,
        nullable=False
    )

    property = db.Column(
        db.Integer,
        db.ForeignKey('properties.id')
    )

    booker = db.Column(
        db.Text,
        db.ForeignKey('users.username')
    )




def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)