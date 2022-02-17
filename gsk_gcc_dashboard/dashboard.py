# imports


import dash
import dash_bootstrap_components as dbc
from flask import current_app as app

# Initiate logger
log = app.logger
from . import callbacks,layout



def init_dashboard(server=None):
    # The dashboard should ideally be initialized from the main init file, with the server passed as a parameter. However, for unit testing, the dashboard can be called directly as well by executing this file
    app_server = (
        server if server is not None else True
    )  # When true, a server is created

    dash_app = dash.Dash(
        name=__name__,
        server=app_server,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=[dbc.themes.BOOTSTRAP]#'/static/src/stylebg.css'
    )

    log.debug("Dash board will be started now")
    # Create Dash Layout

    dash_app.layout = layout.html_layout


    # Define callbacks
    callbacks.init_callbacks(dash_app)
    return dash_app.server



if __name__ == "__main__":
    dash_app = init_dashboard()
    dash_app.run_server(debug=True, threaded=True,)
    #dash_app.run_server(debug=True)