from flask import Blueprint
from flask import render_template
from flask import request

view_bp = Blueprint('view', __name__)

@view_bp.route("/")
def index():
    return render_template("index.html")

@view_bp.route("/attraction/<id>")
def show_attraction(id):
    return render_template("attraction.html")

@view_bp.route("/booking")
def booking():
    return render_template("booking.html")

@view_bp.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")