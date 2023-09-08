import jwt
import os
from dotenv import load_dotenv

load_dotenv()


def encode_jwt(username, first_name, last_name):
    """takes in a username and returns a jwt token that
    includes the username."""

    return jwt.encode({
        "username":username,
        "first_name":first_name,
        "last_name":last_name,
                    },
        os.environ['SECRET_KEY'],
        algorithm='HS256')

def verify_and_decode_jwt(jwt):
    """takes in a jwt and returns the payload as a dictionary"""

    return jwt.decode(
        jwt,
        os.environ['SECRET_KEY'],
        algorithm='HS256')

