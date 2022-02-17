from flask import current_app as app
from flask_assets import Bundle, Environment

# Initiate logger
log = app.logger


def compile_assets(assets):

    bundles = {
        "main_js": Bundle(
            "src/js/lib/jquery-3.6.0.min.js",
            "src/js/lib/popper.min.js",
            "src/js/lib/bootstrap.min.js",
            filters="jsmin",
            output="dist/js/main.min.js",
        ),
        "main_css": Bundle(
            "src/css/lib/bootstrap.min.css",
            filters="cssmin",
            output="dist/css/main.min.css",
            extra={"rel": "stylesheet/css"},
        )
        # Can also refer to blueprints when loading css (main_bp/*.css)
    }
    for name, bundle in bundles.items():
        assets.register(name, bundle)

        # When in dev, build. When in prod, source from CDNs
        if app.config["FLASK_ENV"] == "development":
            bundle.build()



