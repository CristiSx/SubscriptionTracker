from flask import Blueprint

subscriptions = Blueprint('subscriptions', __name__)

@subscriptions.route("/dashboard")
def dashboard():
    return "<h1>Dashboard OK</h1>"