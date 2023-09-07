import os
from dotenv import load_dotenv

from flask import Flask, request, jsonify

from forms import PostLogin, PostRegister, PatchUser
from forms import PostCreateBooking, PostSendMessage, PostListProperty
from models import db, connect_db, User, Property, Message, Booking, Photo

from flask_cors import CORS

import boto3

load_dotenv()

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