from flask import Blueprint, render_template
from . import data
from . import analysis as an

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    return render_template("home.html")


@bp.route("/analysis")
def analysis():
    return render_template("analysis.html")
