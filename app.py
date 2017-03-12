#!flask/bin/python
from flask import Flask, jsonify, request, make_response, redirect, session, url_for, abort
from oauth2client import client, crypt
import datetime, uuid, jwt, json, pprint

from dbController import insertUser, existUser, getPasswordHash
from authenticator import encodeAuthToken, decodeAuthToken, hashPassword, verifyPassword
from constants import EMAIL, PASSWORD, AUTHORIZATION, SECRET_KEY, \
	TOKEN_VALID_TIME, CLIENT_ID, TOKEN_RESPONSE, ID_TOKEN, CURRENT

app = Flask(__name__)
counter = 0

def authenticateWithGoogle():	
	flow = client.flow_from_clientsecrets(
			'client_secrets.json',
			scope='email',
			redirect_uri=url_for('authenticate', _external=True))
	if 'code' not in request.args:
		print "19"
		auth_uri = flow.step1_get_authorize_url()
		return redirect(auth_uri)
	else:
		auth_code = request.args.get('code')
		credentials = flow.step2_exchange(auth_code)
		if credentials:
			id_token = _extractIdToken(credentials.to_json())
			if id_token is not None:
				token = credentials.get_access_token()
				return _constructTokenResponse(id_token, token.expires_in)
			else:
				abort(401)
		else:
			abort(401)

@app.route('/v1/authenticate', methods=['GET', 'POST'])
def authenticate():
	if request.method == 'POST' and request.json is not None and _validRequest(request.json):
		print "33"
		if existUser(request.json[EMAIL]):
			print "35"
			if verifyPassword(request.json[PASSWORD], getPasswordHash(request.json[EMAIL])):
				return _constructTokenResponse(encodeAuthToken(request.json[EMAIL]), TOKEN_VALID_TIME)
			else:
				abort(401)
		else:
			insertUser(request.json[EMAIL], hashPassword(request.json[PASSWORD]))
			return _constructTokenResponse(encodeAuthToken(request.json[EMAIL]), TOKEN_VALID_TIME)
	else:
		print "44"
		return authenticateWithGoogle()
		
@app.route('/v1/current', methods=['GET', 'PUT'])
def current():
	if _userAuthenticated():
		global counter 
		if request.method == 'PUT' and CURRENT in request.form:
			try:
				counter = int(request.form[CURRENT])
			except:
				abort(400)
		return _constructCounterResponse(counter)
	else:
		abort(401)
		
@app.route('/v1/next', methods=['GET'])
def next():
	if _userAuthenticated():
		global counter 
		counter = counter + 1	
		return _constructCounterResponse(counter)
	else:
		abort(401)
		
@app.errorhandler(401)
def custom_401(error):
	return make_response(jsonify({'WWWAuthenticate':'Basic realm="Login Required"'}), 401)
	
@app.errorhandler(400)
def custom_400(error):
	return make_response(jsonify({'status': 'failed', \
	'message': 'Bad Request.  PUT must contain an integer for \"current\".'}), 401)
	
def _constructCounterResponse(counter):
	return make_response(jsonify({"data": { "type": "counter", "id": counter }}), 200)	

def _constructTokenResponse(token, expiresIn):
	return make_response(jsonify({ \
		"data": { \
			"type": "token", \
			"id": datetime.datetime.utcnow(), \
			"attributes": { \
				"access_token": token, \
				"token_type": "Bearer", \
				"expires_in": expiresIn \
			} \
		} \
	}), 200)	
	
def _validRequest(body):
	return body[EMAIL] is not None and body[PASSWORD] is not None 
	
def _userAuthenticated():
	if AUTHORIZATION in request.headers:
		tokenArr = request.headers[AUTHORIZATION].split(' ')
		if len(tokenArr) == 2:
			if existUser(decodeAuthToken(tokenArr[1])):
				return True
			else:
				try:
					idinfo = client.verify_id_token(tokenArr[1], CLIENT_ID)
					if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
						abort(401)		
					else:
						return True
				except crypt.AppIdentityError:
					abort(401)
		else:
			return False
	else:
		abort(401)

def _extractIdToken(data):
	d = json.loads(data)
	if TOKEN_RESPONSE in d and ID_TOKEN in d[TOKEN_RESPONSE]:
		return d[TOKEN_RESPONSE][ID_TOKEN]
	return None
	
if __name__ == '__main__':
	app.secret_key = SECRET_KEY
	app.run(host='0.0.0.0',debug=True)
	