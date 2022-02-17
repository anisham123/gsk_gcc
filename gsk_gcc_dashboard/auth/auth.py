# auth.py
from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
import sys
sys.path.append('../..')
from gsk_gcc_dashboard import db, login_manager
from .models import User



auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    print('UserID',user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page.")
    return redirect(url_for("auth_bp.login"))


@auth_bp.route("/login")
def login():
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not user.check_password(password):
        flash("Please check your login details and try again.")
        return redirect(
            url_for("auth_bp.login")
        )  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for("home_bp.index"))


@auth_bp.route("/signup")
def signup():
    return render_template("signup.html")


@auth_bp.route("/signup", methods=["POST"])
def signup_post():

    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    user = User.query.filter_by(
        email=email
    ).first()  # if this returns a user, then the email already exists in database

    if (
        user
    ):  # if a user is found, we want to redirect back to signup page so user can try again
        flash("Email address already exists")
        return redirect(url_for("auth_bp.signup"))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name)
    new_user.set_password(password)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth_bp.login"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home_bp.index"))

