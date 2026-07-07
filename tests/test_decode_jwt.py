from scripts import decode_jwt
import os
import jwt
import pytest

def test_valid_secret():
    VALID_SECRET = os.environ.get("MY_SECRET_KEY")
    token = decode_jwt.create_token(VALID_SECRET)

    decoded_data = jwt.decode(token, VALID_SECRET, algorithms=["HS256"])
    assert decoded_data["sub"] == "dana"

def test_in_valid_secret():
    INVALID_SECRET = "i.am.invalid.secret"
    VALID_SECRET = os.environ.get("MY_SECRET_KEY")
    token = decode_jwt.create_token(INVALID_SECRET)
    with pytest.raises(jwt.exceptions.InvalidSignatureError):
        jwt.decode(token, VALID_SECRET, algorithms=["HS256"])    





