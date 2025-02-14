from flask import Blueprint, flash, render_template, request
from werkzeug.security import generate_password_hash

from app.models import db
from app.models.user_model import User

user_bp = Blueprint("user", __name__, url_prefix="/")


@user_bp.route("/users", methods=["GET"])
def show_users():
    users = User.query.all()
    return render_template("users.html", users=users)


@user_bp.route("/signup", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data.get("name") or not data.get("email") or not data.get("password"):
        flash("Missing required fields", "error")
        return render_template("signup.html")

    if User.query.filter_by(name=data["name"]).first():
        flash("Name already exists", "error")
        return render_template("signup.html")

    if User.query.filter_by(email=data["email"]).first():
        flash("Email already exists", "error")
        return render_template("signup.html")

    # パスワードをハッシュ化
    hashed_password = generate_password_hash(data["password"])

    new_user = User(name=data["name"], email=data["email"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return render_template("users.html")


@user_bp.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")
