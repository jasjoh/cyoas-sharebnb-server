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

    auth_header = request.headers.get('authorization')
    print('add_user_to_g() called with auth_header', auth_header)

    if auth_header == None:
        g.user = None

    else:
        try:
            token = auth_header.split(' ')[1]
            user = verify_and_decode_jwt(token)
            print("adding user to g", user)
            g.user = user

        except (jwt.exceptions.InvalidTokenError, jwt.exceptions.DecodeError):
            print("attempting to decode tokens threw exception")
            g.user = None



@app.route('/auth/register', methods=["POST"])
def signup():
    """Handle user signup.

    Create new user, add to DB and return token.

    If form is invalid, return invalid request (ideally with invalid fields)

    If the there already is a user with that username, return appropriate error
    """


    form_data_dict = {
        "username": request.json["username"],
        "password": request.json["password"],
        "first_name": request.json["firstName"],
        "last_name": request.json["lastName"],
    }

    form_data_list = [(k, v) for k, v in form_data_dict.items()]
    form_data_multi_dict = MultiDict(form_data_list)

    print("form data to be injected into form:", form_data_multi_dict)

    form = PostRegister(formdata=form_data_multi_dict, csrf_enabled=False)

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
def post_lucky_num():
    """
    """
    # print('request.json', request.json)
    print('request.form', request.form)
    print('request.args', request.args)
    print('request.files', request.files)
    # generate form data for validation using JSON from request
    form_data = {
        "image_file": request.files["imageFile"],
        "description": request.form["description"],
        "title": request.form["title"],
        "price": request.form["price"],
    }

    form = PostListProperty(data=form_data, csrf_enabled=False)

    if form.validate_on_submit():
        # if we make it here, form passes WTForms validation
        # step 1: fetch image from form
        f = form.image_file.data
        print('f', f)
        print('f.filename', f.filename)
        # step 2: upload image to s3 and get URL
        s3 = boto3.resource('s3')
        s3.Bucket(S3_BUCKET_NAME).put_object(Key=f.filename, Body=f, ContentType=f.content_type)

        url = f'https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{f.filename}'

        response = {'url': url}

        return (jsonify(response), 201)

    return (jsonify({'Errors': 'An error occured'}), 400)