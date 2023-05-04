"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token, jwt_required
import hashlib

api = Blueprint('api', __name__)

@api.route('/signup', methods=['POST'])
def signup():
   
    data = request.get_json()

    
    if not data.get('email') or not data.get('password'):
        response_body = {'message': 'Email and password are required.'}
        return jsonify(response_body), 400
  
    if User.query.filter_by(email=data['email']).first():
        response_body = {'message': 'A user with this email already exists.'}
        return jsonify(response_body), 409

    hashed_password = hashlib.sha256(data['password'].encode('utf-8')).hexdigest()
    new_user = User(email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    response_body = {'message': 'User created successfully.'}
    return jsonify(response_body), 201


@api.route('/login', methods=['POST'])
def login():
   
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        response_body = {'message': 'Email and password are required.'}
        return jsonify(response_body), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user:
        response_body = {'message': 'Invalid email or password.'}
        return jsonify(response_body), 401

    if hashlib.sha256(data['password'].encode('utf-8')).hexdigest() != user.password:
        response_body = {'message': 'Invalid email or password.'}
        return jsonify(response_body), 401

    access_token = create_access_token(identity=str(user.id))

    response_body = {'message': 'Login successful.', 'access_token': access_token}
    return jsonify(response_body), 200


@api.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    """
    Route for getting the current user's information.
    Requires an access token in the request headers.
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    response_body = {'email': current_user.email}
    return jsonify(response_body), 200


@app.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    current_user_id = get_jwt_identity()
    files = request.files.getlist('files')
    for file in files:
        new_file = File(name=file.filename, data=file.read(),user_id=current_user_id)
        db.session.add(new_file)
    db.session.commit()
    return jsonify({'message': f'{len(files)} files uploaded successfully!'})

@app.route('/files', methods=['GET'])
@jwt_required()
def get_files():
    files = File.query.all()
    return jsonify([file.serialize() for file in files])



