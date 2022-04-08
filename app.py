# flask imports
from shutil import ExecError
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid # for public id
from werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps


from uuid import uuid4
from datetime import datetime
import json
import boto3
import os


# creates Flask object
app = Flask(__name__)


# configuration
# Hardcoding configuration for now but it is not recommended


app.config['SECRET_KEY'] = '61c8e74bdeb544b9a7ff99e80060eabb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# creates SQLALCHEMY object
db = SQLAlchemy(app)

# Database ORMs
class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	public_id = db.Column(db.String(50), unique = True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(70), unique = True)
	password = db.Column(db.String(80))



# decorator for verifying the JWT
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None

		# check if jwt is passed in the request header
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']


		# return 401 HTTP Method if token is not passed
		if not token:
			return jsonify({'message' : 'Token is missing !!'}), 401

		try:
			# decoding the payload to fetch the stored details
			print(token)
			print(app.config['SECRET_KEY'])
			data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
			print(data)
			current_user = User.query.filter_by(public_id = data['public_id']).first()
			print("Hello")
		except Exception as e:
			print(e)
			return jsonify({
				'message' : 'Token is invalid !!'
			}), 401
		# returns the current logged in users contex to the routes
		return f(current_user, *args, **kwargs)

	return decorated



# route for logging user in
@app.route('/login', methods =['POST'])
def login():
	# creates dictionary of form data
	auth = request.form

    # querying the database
	if not auth or not auth.get('email') or not auth.get('password'):
		# returns 401 if any detail is missing (email/password)
		return make_response(
			'Could not verify',
			401,
			{'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
		)

	user = User.query\
		.filter_by(email = auth.get('email'))\
		.first()

	if not user:
		# returns 401 if user does not exist
		return make_response(
			'Could not verify',
			401,
			{'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
		)

	if check_password_hash(user.password, auth.get('password')):
		# generates the JWT Token
		token = jwt.encode({
			'public_id': user.public_id,
			'exp' : datetime.utcnow() + timedelta(minutes = 100000000)
		}, app.config['SECRET_KEY'])

		return make_response(jsonify({'token' : token}), 201)


	# returns 403 if password is wrong
	return make_response(
		'Could not verify',
		403,
		{'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
	)



# signup route
@app.route('/signup', methods =['POST'])
def signup():
	# creates a dictionary of the form data
	data = request.form

	# gets name, email and password
	name, email = data.get('name'), data.get('email')
	password = data.get('password')

	# checking for existing user
	user = User.query\
		.filter_by(email = email)\
		.first()
	if not user:
		# database ORM object
		user = User(
			public_id = str(uuid.uuid4()),
			name = name,
			email = email,
			password = generate_password_hash(password)
		)
		# insert user
		db.session.add(user)
		db.session.commit()

		return jsonify({'status': 'success'})
	else:
		# returns 202 if user already exists
		return make_response('User already exists. Please Log in.', 202)


# create file route
@app.route('/create_file', methods=['POST'])
@token_required
def create_file(current_user):

	data = {}

	post_data = request.form
	body = post_data.get('body')

	data['uuid'] = str(uuid4())
	data['created_by'] = current_user.name
	data['created_time'] = str(datetime.now())
	data['modified_by'] = current_user.name
	data['modified_time'] = str(datetime.now())
	data['body'] = str(body)

	file_data = json.dumps(data, indent = 4)
	file_name = str(data['uuid']) + '.json'

	# create file and write data to it
	with open(file_name, 'w') as f:
		f.write(file_data)

	s3_client = boto3.client("s3", endpoint_url="http://0.0.0.0:4566", aws_access_key_id="temp", aws_secret_access_key="temp")

	# upload file to s3
	s3_client.upload_file(file_name, "localbucket", file_name)

	# delete file
	os.remove(file_name)

	return jsonify(data)


# get file route
@app.route('/get_file', methods=['POST'])
@token_required
def get_file(current_user):
	
	try:
		data = {}

		post_data = request.form
		file_name = post_data.get('file_name')

		s3_client = boto3.client("s3", endpoint_url="http://0.0.0.0:4566", aws_access_key_id="temp", aws_secret_access_key="temp")

		# download file from s3
		s3_client.download_file("localbucket", file_name, file_name)

		# read file
		with open(file_name, 'r') as f:
			data = json.load(f)
		
		# delete file
		os.remove(file_name)

		return jsonify(data)
	except:
		return jsonify({'status': 'Invalid File Name or File does not exists'})


# update file route
@app.route('/update_file', methods=['POST'])	
@token_required
def update_file(current_user):
	
	data = {}

	post_data = request.form
	file_name = post_data.get('file_name')
	body = post_data.get('body')

	s3_client = boto3.client("s3", endpoint_url="http://0.0.0.0:4566", aws_access_key_id="temp", aws_secret_access_key="temp")

	# download file from s3
	s3_client.download_file("localbucket", file_name, file_name)

	# read file
	with open(file_name, 'r') as f:
		data = json.load(f)
	
	# update file
	data['body'] = str(body)
	data['modified_by'] = current_user.name
	data['modified_time'] = str(datetime.now())

	# write file
	with open(file_name, 'w') as f:
		f.write(json.dumps(data, indent = 4))

	# upload file to s3
	s3_client.upload_file(file_name, "localbucket", file_name)

	# delete file
	os.remove(file_name)

	return jsonify(data)


# delete file route
@app.route('/delete_file', methods=['POST'])
@token_required
def delete_file(current_user):
	
	data = {}

	post_data = request.form
	file_name = post_data.get('file_name')

	s3_client = boto3.client("s3", endpoint_url="http://0.0.0.0:4566", aws_access_key_id="temp", aws_secret_access_key="temp")

	# download file from s3
	s3_client.download_file("localbucket", file_name, file_name)

	# delete file
	os.remove(file_name)

	return jsonify(data)



if __name__ == "__main__":
	# setting debug to True enables hot reload
	# and also provides a debugger shell
	# if you hit an error while running the server
	app.run(debug = True)


