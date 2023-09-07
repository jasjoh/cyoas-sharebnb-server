
from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):

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

    #class methods for signup and authenticate


class Properties(db.Model):

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

class Photos(db.Model):

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


class Messages(db.Model):

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


class Bookings(db.Model):

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