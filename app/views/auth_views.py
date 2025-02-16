from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from app.models.user_model import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    data = request.form
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        flash("Missing required fields", "error")
        return render_template("login.html"), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("User does not exist", "error")
        return render_template("login.html"), 400
    if not check_password_hash(user.password, password):
        flash("Invalid password")
        return render_template("login.html"), 400

    if not login_user(user):
        flash("login failed. This user might be inactive")
        return render_template("login.html"), 400

    return redirect(url_for("user.home"))


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
