from flask import Blueprint, request, current_app, jsonify, make_response
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas import RegisterSchema, LoginSchema
from models import User
from utils import json_error, hash_password, verify_password, generate_jwt, set_jwt_cookie

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.post("/register")
def register():
    data = request.get_json() or {}
    errors = RegisterSchema().validate(data)
    if errors:
        return json_error(errors, 400)

    db: Session = current_app.session()
    existing = db.scalars(select(User).where(User.email == data["email"])) .first()
    if existing:
        return json_error("Email already registered", 400)

    user = User(email=data["email"], password_hash=hash_password(data["password"]), name=data.get("name"))
    db.add(user)
    db.commit()
    return jsonify({"message": "Registered successfully"}), 201


@bp.post("/login")
def login():
    data = request.get_json() or {}
    errors = LoginSchema().validate(data)
    if errors:
        return json_error(errors, 400)

    db: Session = current_app.session()
    user = db.scalars(select(User).where(User.email == data["email"])) .first()
    if not user or not verify_password(data["password"], user.password_hash):
        return json_error("Invalid credentials", 401)

    token = generate_jwt({"sub": user.id, "email": user.email, "is_admin": user.is_admin}, current_app.config["SECRET_KEY"])
    resp = make_response({"token": token})
    set_jwt_cookie(resp, token, current_app.config["JWT_COOKIE_SECURE"])
    return resp
