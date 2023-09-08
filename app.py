import os
from dotenv import load_dotenv

from flask import Flask, request, jsonify, g, session

from forms import PostLogin, PostRegister, PatchUser
from forms import PostCreateBooking, PostSendMessage, PostListProperty

from models import db, connect_db, User, Property, Message, Booking, Photo
from sqlalchemy.exc import IntegrityError
import jwt
from auth import encode_jwt, verify_and_decode_jwt

from werkzeug.datastructures import MultiDict


from flask_cors import CORS

import boto3

load_dotenv()

CURR_USER_KEY = "curr_user"


app = Flask(__name__)
CORS(app)

S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
AWS_REGION = os.environ['AWS_REGION']

DEFAULT_IMAGE_URL = ( f'https://{S3_BUCKET_NAME}.s3.{AWS_REGION}'
                     f'.amazonaws.com/craterhoof_4x6.jpg')

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_ECHO'] = True
app.config['WTF_CSRF_ENABLED'] = False

connect_db(app)

@app.before_request
def add_user_to_g():
    """Grabs the auth header, and if a token exists, verifies, decodes, and
    assigns its payload to g.user.  ex:  {username, first_name, last_name} """

    # auth_header = request.headers.get('authorization')
    # print('add_user_to_g() called with auth_header', auth_header)

    # if auth_header == None:
    #     g.user = None

    # else:
    #     try:
    #         token = auth_header.split(' ')[1]
    #         user = verify_and_decode_jwt(token)
    #         print("adding user to g", user)
    #         g.user = user

    #     except (jwt.exceptions.InvalidTokenError, jwt.exceptions.DecodeError):
    #         print("attempting to decode tokens threw exception")
    #         g.user = None

    # TODO: Hardcoded User
    g.user = {
        'username': 'username',
        'first_name': 'First Name',
        'last_name': 'Last Name'
    }



@app.route('/auth/register', methods=["POST"])
def signup():
    """Handle user signup.

    Create new user, add to DB and return token.

    If form is invalid, return invalid request (ideally with invalid fields)

    If the there already is a user with that username, return appropriate error
    """

    form_data = MultiDict([
        ("username", request.json["username"]),
        ("password", request.json["password"]),
        ("first_name", request.json["firstName"]),
        ("last_name", request.json["lastName"]),
    ])

    print("form data to be injected into form:", form_data)

    form = PostRegister(formdata=form_data, csrf_enabled=False)

    if form.validate():
        # all form data was valid
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
            )
            print("user should be good")
            db.session.commit()

        except IntegrityError as exc:
            # username already existed in database
            print("integrity error:", exc)
            print("signup() called but username already in database")
            return (jsonify({"errors": [ "Username already taken" ]}), 400)

        token = encode_jwt(
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        print("token returned from signup()", token)

        token_dict = { 'token': token }

        return jsonify(token_dict, 201)

    else:
        # form.field = [ fields ]
        # field.errors = [ error message ]
        for field, errorMsgs in form.errors.items():
            for err in errorMsgs:
                print("form field with errors:", field)
                print("error message:", err)

        return (jsonify({"errors": [ "To be figured out" ]}), 400)



@app.post("/properties")
def post_properties():
    """
    """
    # print('request.json', request.json)
    print('request.form', request.form)
    print('request.args', request.args)
    print('request.files', request.files)
    # generate form data for validation using JSON from request

    form_data = MultiDict([
        ('photo_primary_file', request.files["photoPrimaryFile"]),
        ('photo_primary_name', request.form["photoPrimaryName"]),
        ('description', request.form["description"]),
        ('title', request.form["title"]),
        ('price_per_day', request.form["pricePerDay"]),
    ])

    form = PostListProperty(formdata=form_data, csrf_enabled=False)

    if form.validate_on_submit():
        # if we make it here, form passes WTForms validation
        # step 1: fetch image from form
        file = form.photo_primary_file.data
        url = upload_to_s3(file)

        property = Property(
            title=form.title.data,
            description=form.description.data,
            price_per_day_cents=int(form.price_per_day.data) * 100,
            host_username=g.user['username'],
        )
        db.session.add(property)
        db.session.commit()

        photo = Photo(
            name=form.photo_primary_name.data,
            property_id=property.id,
            url=url
        )
        db.session.add(photo)
        db.session.commit()

        breakpoint()

        response = {
            'property':  {
                'id': property.id,
                'title': property.title,
                'description': property.description,
                'pricePerDay': property.price_per_day_cents / 100,
                'host': property.host_username,
                'photoPrimaryName': property.photo_primary[0].name,
                'photoPrimaryUrl': property.photo_primary[0].url,
            }
        }

        return (jsonify(response), 201)

    return (jsonify({'Errors': 'An error occured'}), 400)

@app.get('/properties')
def get_properties():
    """ Endpoint to get all the properties """
    properties = Property.query.all()
    propertiesResponse = [{
        'id': property.id,
        'title': property.title,
        'description': property.description,
        'pricePerDay': property.price_per_day_cents / 100,
        'host': property.host_username,
        'photoPrimaryName': property.photo_primary[0].name,
        'photoPrimaryUrl': property.photo_primary[0].url,
    } for property in properties]

    print("propertiesResponse after mapping:", propertiesResponse)

    return (jsonify({ 'properties': propertiesResponse }))

@app.delete('/properties/<int:id>')
def delete_property(id):
    property = Property.query.get_or_404(id)
    db.session.delete(property)
    db.session.commit()
    return (jsonify({ 'message': 'Property Deleted'}))

def upload_to_s3(file):
    """ Uploads a file to S3 and returns its URL """
    print('upload_to_s3() call with file', file)
    print('file.filename', file.filename)
    s3 = boto3.resource('s3')
    s3.Bucket(S3_BUCKET_NAME).put_object(
        Key=file.filename, Body=file, ContentType=file.content_type)

    return (f'https://{S3_BUCKET_NAME}.s3'
            f'.{AWS_REGION}.amazonaws.com/{file.filename}')
