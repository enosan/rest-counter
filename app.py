#!flask/bin/python
from flask import Flask, jsonify, request, make_response, redirect, session, url_for, abort
from oauth2client import client
import datetime, uuid, jwt

from dbController import insertUser, existUser, passwordMatch
from authenticator import encodeAuthToken, decodeAuthToken, hashPassword
from constants import EMAIL, PASSWORD, SECRET_KEY

app = Flask(__name__)
counter = 0

@app.route('/v1/authenticate', methods=['GET'])
def authenticateWithGoogle():	
	flow = client.flow_from_clientsecrets(
			'client_secrets.json',
			scope='email',
			redirect_uri=url_for('authenticateWithGoogle', _external=True))
	if 'code' not in request.args:
		auth_uri = flow.step1_get_authorize_url()
		return redirect(auth_uri)
	else:
		auth_code = request.args.get('code')
		credentials = flow.step2_exchange(auth_code)
		if credentials and credentials.token_response and credentials.token_response.access_token:
			return credentials.token_response.access_token
		else:
			abort(401)

@app.route('/v1/authenticate', methods=['POST'])
def authenticate():
	if request.json is not None and _validRequest(request.json):
		if existUser(request.json[EMAIL]):
			if passwordMatch(request.json[EMAIL], hashPassword(request.json[PASSWORD])):
				return encodeAuthToken(request.json[EMAIL], request.json[PASSWORD])
			else:
				abort(401)
		else:
			insertUser(request.json[EMAIL], hashPassword(request.json[PASSWORD]))
			return encodeAuthToken(request.json[EMAIL], request.json[PASSWORD])
	else:
		abort(401)
		
@app.route('/v1/current', methods=['GET'])
def current():
	if _userAuthenticated():
		global counter 
		return constructResponse(counter)
	else:
		abort(401)
		
@app.route('/v1/next', methods=['GET'])
def next():
	if _userAuthenticated():
		global counter 
		counter = counter + 1	
		return _constructResponse(counter)
	else:
		abort(401)

@app.errorhandler(401)
def custom_401(error):
	return make_response(jsonify({'WWWAuthenticate':'Basic realm="Login Required"'}), 401)
	
def _constructResponse(counter):
	return jsonify({"data": { "type": "counter", "id": counter }})	
	
def _validRequest(body):
	return body[EMAIL] is not None and body[PASSWORD] is not None 
	
def _userAuthenticated():
	return True
	
if __name__ == '__main__':
	app.secret_key = SECRET_KEY
	app.run(host='0.0.0.0',debug=True)
	