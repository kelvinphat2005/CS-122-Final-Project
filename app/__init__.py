import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    # instantiate database (SQLite)
    app.config["DATABASE"] = os.path.join(app.instance_path, "main.db")
    os.makedirs(app.instance_path, exist_ok=True) # create instance folder

    # db setup: auto close connections, create tables, add `flask init-db`
    from . import data
    data.init_app(app)

    # register routes/pages
    from .routes import bp
    app.register_blueprint(bp)

    return app
