from flask import Blueprint
from flask import render_template
from flask import request
import requests

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

@view_bp.route("/thankyou/<order_number>")
def thankyou(order_number):
    base_url = request.base_url.split('/thankyou')[0]
    response = requests.get(base_url + '/api/order/' + order_number).json()

    if len(response['data']) > 0:
        return render_template("thankyou.html", result = '恭喜預定成功')
    else:
        return render_template("thankyou.html", result = '無此訂單編號，請重新預定')
    
