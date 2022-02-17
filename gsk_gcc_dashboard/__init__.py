import dash
from flask import Flask, app
from flask_assets import Environment
from flask_login import LoginManager, login_required, current_user
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy & login so we can use it later in our models
db = SQLAlchemy()
login_manager = LoginManager()
assets = Environment() #Compile & manage statis assets


def protect_dash_views(app):
    """
    Helper function to secure all dash functions - no access without Login. Separate function required since there are no direct routes available when rendering layouts (only available for callbacks)
    """
    for view_func in app.view_functions:
        if view_func.startswith(
            "/dashapp"
        ):  # Assumes all dash views start with /dashapp (True atm)
            app.view_functions[view_func] = login_required(
                app.view_functions[view_func]
            )

    return app


def init_app(config):
    """
    Initiating web app dependencies here

    Files used
    ----------
    config : dict
        Dictionary containing variables required for the application

    Returns
    -------
    app: Flask
        A flask application with all blueprints, routes and dashboard
    """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config)
    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize asset plugins
    assets.init_app(app)

    with app.app_context():
        # Import parts of our core Flask app
        from .auth import auth
        from .home import home
        # Create sql tables for our data models
        db.create_all()

        # Initialize login_manager
        login_manager.login_view = "auth.login"
        login_manager.init_app(app)

        # Register assets
        from .routes import compile_assets

        compile_assets(assets)

        # Register blueprints
        app.register_blueprint(auth.auth_bp)  # blueprint for auth routes in our app
        app.register_blueprint(home.home_bp)  ## blueprint for non-auth parts of app

        # Initiate dashboard
        from . import dashboard
        print("app",current_user)

        app = dashboard.init_dashboard(app)
        # Secure the dash views (Auth access only)
        app = protect_dash_views(app)

        return app
