#!/bin/python
import datetime, jwt
from passlib.hash import pbkdf2_sha256
from constants import TOKEN_VALID_TIME, SECRET_KEY

def encodeAuthToken(email):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=TOKEN_VALID_TIME),
            'iat': datetime.datetime.utcnow(),
            'sub': email
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decodeAuthToken(auth_token):
    try:
        payload = jwt.decode(auth_token, SECRET_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def hashPassword(password):
	return pbkdf2_sha256.hash(password)

def verifyPassword(password, hash):
	return pbkdf2_sha256.verify(password, hash)