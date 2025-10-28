import time
import jwt
from flask import request, jsonify
from passlib.hash import pbkdf2_sha256


def json_error(message, status=400):
    return jsonify({"error": message}), status


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed)


def generate_jwt(payload: dict, secret: str, exp_seconds: int = 3600):
    data = payload.copy()
    data["exp"] = int(time.time()) + exp_seconds
    return jwt.encode(data, secret, algorithm="HS256")


def decode_jwt(token: str, secret: str):
    return jwt.decode(token, secret, algorithms=["HS256"])


def set_jwt_cookie(resp, token: str, secure: bool):
    resp.set_cookie(
        "access_token",
        token,
        httponly=True,
        secure=secure,
        samesite="Strict",
        max_age=3600,
        path="/",
    )


def get_token_from_request():
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth.split(" ", 1)[1]
    return request.cookies.get("access_token")
