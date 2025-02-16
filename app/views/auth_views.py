from flask import Blueprint, flash, render_template, request


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
    return render_template("home.html")
