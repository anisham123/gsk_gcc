"""Application entry point."""
import json
import os

from config import DevConfig
from gsk_gcc_dashboard import init_app

#Define configuration parameters
config = DevConfig()


#Initialize app
app = init_app(config=config)

if __name__ == "__main__":
    #Run in prod mode
    app.run(host='0.0.0.0', debug=False)
