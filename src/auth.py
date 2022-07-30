from flask import Blueprint, jsonify, request
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)
import validators
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    create_access_token,
    create_refresh_token,
)
from src.database import db, User


auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth.post('/register')
def register():
    username = request.json.get('username', '')
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    if len(password) < 6:
        return jsonify({
            'error': 'Password is too short'
        }), 400

    if len(username) < 3:
        return jsonify({
            'error': 'Username is too short'
        }), 400
    
    if not username.isalnum():
        return jsonify({
            'error': 'Username must be alphanumeric'
        }), 400
    
    if not validators.email(email):
        return jsonify({
            'error': 'Email is not valid'
        }), 400
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({
            'error': 'Email is taken'
        }), 409 # 409 confilict

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({
            'error': 'Username is taken'
        }), 409 # 409 confilict
    
    password_hashed = generate_password_hash(password)
    user = User(username=username, password=password_hashed, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User created',
        'user': {
            'usename': username,
            'email': email,
        }
    }), 201


@auth.post('/login')
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    errors = []

    # handle empty or non-existance fields
    if not email:
        errors.append({
            'email': 'email field is required',
        })
    
    if not password:
        errors.append({
            'password': 'password field is required',
        })
    
    if errors:
        return {
            'errors': errors,
        }, 400

    user = User.query.filter_by(email=email).first()

    if user:
        password_correct = check_password_hash(user.password, password)

        if password_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'refresh': refresh,
                'access': access,
            }), 200

    return jsonify({
        'error': 'Wrong credentials'
    }), 401


@auth.post('/token/refresh')
@jwt_required(refresh=True)
def refresh_user_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return {
        'access': access
    }, 200
