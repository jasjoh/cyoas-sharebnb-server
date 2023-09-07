from flask_wtf import FlaskForm
from wtforms import FileField, StringField, IntegerField



class PostListProperty(FlaskForm):

    image_file = FileField(
        'Image file',
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
