from flask import Blueprint, jsonify, render_template, request
from werkzeug.security import generate_password_hash

from app.models import db
from app.models.user_model import User

user_bp = Blueprint("user", __name__, url_prefix="/users")
signup_bp = Blueprint("signup", __name__, url_prefix="/signup")


@user_bp.route("", methods=["GET"])
def get_users():
    users = User.query.all()
    users_list = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "is_active": user.is_active,
        }
        for user in users
    ]
    return jsonify(users_list), 200


@user_bp.route("", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "Name already exists"}), 409

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 409

    # パスワードをハッシュ化
    hashed_password = generate_password_hash(data["password"])

    new_user = User(name=data["name"], email=data["email"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(
        {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "is_active": new_user.is_active,
        }
    ), 201


@signup_bp.route("", methods=["GET"])
def signup():
    return render_template("signup.html")
