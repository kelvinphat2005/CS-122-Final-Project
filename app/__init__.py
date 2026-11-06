import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    # instantiate database (SQLite)
    app.config["DATABASE"] = os.path.join(app.instance_path, "main.db")
    os.makedirs(app.instance_path, exist_ok=True) # create instance folder

    # auto close db
    from . import data
    app.teardown_appcontext(data.close_db)

    # register routes/pages
    from .routes import bp
    app.register_blueprint(bp)

    return app
