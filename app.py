from flask import Flask, request, jsonify
from forms import PostListProperty
from requests.exceptions import HTTPError
import boto3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['WTF_CSRF_ENABLED'] = False

# Flask WTF File Forms
# https://flask-wtf.readthedocs.io/en/0.15.x/form/#file-uploads



# Jesse's Config
BUCKET_NAME = 'rithm-r32-jesjas-sharebnb-jes'
REGION = 'us-east-2'

# Jason's Config
# BUCKET_NAME = 'rithm-r32-jesjas-sharebnb-jas'
# REGION = 'us-west-1'

@app.post("/properties")
def get_lucky_num():
    """
    """
    # print('request.json', request.json)
    # print('request.form', request.form)
    # print('request.args', request.args)
    # print('request.files', request.files)
    # generate form data for validation using JSON from request
    form_data = {
        "image_file": request.files["image_file"],
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
        s3.Bucket(BUCKET_NAME).put_object(Key=f.filename, Body=f, ContentType=f.content_type)

        url = f'https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{f.filename}'

        response = {'url': url}

        return (jsonify(response), 201)

    return (jsonify({'Errors': 'An error occured'}), 400)