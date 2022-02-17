from flask import Blueprint
from flask import current_app as app
from flask import make_response, render_template
from flask_login import current_user, login_required

home_bp = Blueprint(
    "home_bp", __name__, template_folder="templates", static_folder="static"
)

print("Home")
@home_bp.route("/")
@home_bp.route("/home")
@home_bp.route("/index")
@login_required
def index():
    # return "hello world"
    return render_template(
        "index.html", name=current_user.name
    )


@home_bp.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html",
        name=current_user.name,
        email=current_user.email
    )

