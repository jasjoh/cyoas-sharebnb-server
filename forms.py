from flask_wtf import FlaskForm
from wtforms import FileField, StringField, IntegerField, PasswordField
from wtforms.validators import InputRequired, Optional, Length

class PostLogin(FlaskForm):
    """ Form for validating login requests"""

    username = StringField(
        'Username',
        validators=[InputRequired()],
    )

    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=6, max=50)],
    )

class PostRegister(FlaskForm):
    """ Form for validating new user registration requests """

    class Meta:
        csrf = False

    username = StringField(
        'Username',
        validators=[InputRequired()],
    )

    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=6, max=50)],
    )

    first_name = StringField(
        'FirstName',
        validators=[InputRequired()],
    )

    last_name = StringField(
        'LastName',
        validators=[InputRequired()],
    )

class PatchUser(FlaskForm):
    """ Form for validating requests to update a user profile """

    first_name = StringField(
        'First Name',
        validators=[Optional()],
    )

    last_name = StringField(
        'Last Name',
        validators=[Optional()],
    )

class PostCreateBooking(FlaskForm):
    """ Form for validating request to create a new booking """

    start_date = StringField(
        'Start Date',
        validators=[InputRequired()],
    )

    end_date = StringField(
        'End Date',
        validators=[InputRequired()],
    )

    property_id = IntegerField(
        'Property ID',
        validators=[InputRequired()],
    )

class PostSendMessage(FlaskForm):
    """ Form for validating request to send a message """

    text = StringField(
        'Message Text',
        validators=[InputRequired()],
    )

    recipient = StringField(
        'Recipient Username',
        validators=[InputRequired()],
    )

    property_id = IntegerField(
        'Property ID',
        validators=[InputRequired()],
    )

class PostListProperty(FlaskForm):
    """ Form for validating requests to list a new property """

    image_file = FileField(
        'Image file',
        validators=[Optional()],
    )

    description = StringField(
        'Description'
    )

    title = StringField(
        'Title'
    )

    price = IntegerField(
        'Price'
    )
