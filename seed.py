"""Seed database with sample data ."""

from app import db
from models import db, connect_db, User, Property, Message, Booking, Photo

db.drop_all()
db.create_all()

""" FUTURE SEEDING BELOW HERE

like1 = Like(user_id=1, message_id=1)
db.session.add(like1)
db.session.commit()

"""

test_user = User.signup(
        username='username',
        password='password',
        first_name='First Name',
        last_name='Last Name'
    )
db.session.commit()