from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from ..models import User
from .. import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return {"error": "Email already exists"}, 400
    user = User(email=data['email'], name=data['name'],
                password_hash=generate_password_hash(data['password']))
    db.session.add(user)
    db.session.commit()
    return {"msg": "Registered successfully"}

@auth_bp.post("/login")
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return {"error": "Invalid credentials"}, 401
    token = create_access_token(identity=user.id)
    return {"token": token, "user": {"id": user.id, "name": user.name}}
