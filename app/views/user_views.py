from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

from app import db
from app.models.user_model import User

user_bp = Blueprint("user", __name__, url_prefix="/")


@user_bp.route("/", methods=["GET"])
@login_required
def home():
    return render_template("home.html", current_user=current_user)


@user_bp.route("/users", methods=["GET"])
def show_users():
    users = User.query.all()
    return render_template("users.html", users=users)


@user_bp.route("/signup", methods=["POST"])
def create_user():
    data = request.form
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        flash("Missing required fields", "error")
        return render_template("signup.html"), 400

    if User.query.filter_by(name=name).first():
        flash("Name already exists", "error")
        return render_template("signup.html"), 409

    if User.query.filter_by(email=email).first():
        flash("Email already exists", "error")
        return render_template("signup.html"), 409

    # パスワードをハッシュ化
    hashed_password = generate_password_hash(password)

    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("user.show_users"))


@user_bp.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")
