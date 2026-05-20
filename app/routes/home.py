from collections import defaultdict
from datetime import timedelta

from flask import Blueprint, render_template
from flask import request, redirect, url_for
from datetime import datetime
from dateutil.relativedelta import relativedelta

from flask_login import (
    login_required,
    current_user
)

from ..models import OneTimeExpense, Subscription, User
from .. import db

homes = Blueprint("homes", __name__)


@homes.route("/")
@login_required
def home():

    subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    userdata = User.query.filter_by(id=current_user.id).all()

    

    total_spend = sum(sub.cost for sub in subscriptions)

    stats = {
        "monthly_spend": total_spend,

        "active_subscriptions": len(subscriptions),

        "upcoming_bills": 0,

        "average_per_service":
            round(total_spend / len(subscriptions), 2)
            if subscriptions else 0
    }

    return render_template(
        "dashboard.html",
        stats=stats,
        subscriptions=subscriptions,
        userdata=userdata
    )

@homes.route("/view-all")
@login_required
def view_all():
    subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    userdata = User.query.filter_by(id=current_user.id).all()
    cheltuieli = OneTimeExpense.query.filter_by(user_id=current_user.id).all()

    return render_template("viewall.html", subscriptions=subscriptions, userdata=userdata, cheltuieli=cheltuieli)

@homes.route("/projection")
@login_required
def projection():

    subscriptions = Subscription.query.filter_by(
        user_id=current_user.id
    ).all()

    expenses = OneTimeExpense.query.filter_by(
        user_id=current_user.id
    ).all()

    projection_data = defaultdict(float)

    today = datetime.today()

  
    for i in range(12):

        future_date = today + relativedelta(months=i)

        month_name = future_date.strftime("%B %Y")

        # SUBSCRIPTIONS
        for sub in subscriptions:

            if sub.billing_cycle == "monthly":
                projection_data[month_name] += sub.cost

            elif sub.billing_cycle == "yearly":
                projection_data[month_name] += sub.cost / 12

        # ONE TIME EXPENSES
        for expense in expenses:

            expense_month = expense.date.strftime("%B %Y")

            if expense_month == month_name:
                projection_data[month_name] += expense.cost

    return render_template(
        "projection.html",
        labels=list(projection_data.keys()),
        values=list(projection_data.values())
    )

@homes.route("/analytics")
@login_required
def analytics():
    subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    userdata = User.query.filter_by(id=current_user.id).all()
    cheltuieli = OneTimeExpense.query.filter_by(user_id=current_user.id).all()
    return render_template("analytics.html", subscriptions=subscriptions, userdata=userdata, cheltuieli=cheltuieli)

@homes.route("/add-subscription", methods=["POST"])
@login_required
def add_subscription():

    name = request.form.get("name")

    cost = request.form.get("cost")

    billing_cycle = request.form.get("billing_cycle")
    
    first_bill_date = datetime.strptime(request.form.get("first_bill_date"),"%Y-%m-%d").date()

    due_date = datetime.strptime(request.form.get("due_date"),"%Y-%m-%d").date()
    

    subscription = Subscription(
        name=name,
        cost=float(cost),
        billing_cycle=billing_cycle,
        due_date=due_date,
        first_bill_date=first_bill_date,
        user_id=current_user.id
    )

    db.session.add(subscription)

    db.session.commit()


    return redirect(url_for("homes.home"))

@homes.route("/add-one-time-expense", methods=["POST"])
@login_required
def add_one_time_expense():
    name = request.form.get("name")
    cost = request.form.get("cost")
    date = datetime.strptime(request.form.get("date"),"%Y-%m-%d").date()

    one_time_expense = OneTimeExpense(
        name=name,
        cost=float(cost),
        date=date,
        user_id=current_user.id
    )

    db.session.add(one_time_expense)
    db.session.commit()

    return redirect(url_for("homes.home"))