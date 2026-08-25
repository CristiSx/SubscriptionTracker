from datetime import datetime, timedelta

from flask_mail import Message

from .models import Subscription
from . import mail



def check_notifications():

    subscriptions = Subscription.query.all()

    tomorrow = (
        datetime.now().date()
        + timedelta(days=1)
    )

    today = datetime.now().date()

    for sub in subscriptions:

        if not sub.first_bill_date:
            continue

        next_payment = sub.first_bill_date

     
        if sub.billing_cycle == "monthly":

            while next_payment < tomorrow:
                next_payment = next_payment + timedelta(days=30)

       
        elif sub.billing_cycle == "yearly":

            while next_payment < tomorrow:
                next_payment = next_payment.replace(
                    year=next_payment.year + 1
                )

        
        if next_payment == tomorrow:

            msg = Message(

                subject="Alertă reînnoire abonament",

                recipients=[
                    sub.user.email
                ]
            )

            msg.body = f"""
                Salut!

                Abonamentul "{sub.name}"
                se va reînnoi mâine.

                Cost: {sub.cost} $

                Subscription Tracker
                """

            mail.send(msg)

            print(
                f"Email trimis către "
                f"{sub.user.email}"
            )

        
        if (
            sub.due_date
            and sub.due_date == tomorrow
        ):

            msg = Message(

                subject="Încetare abonament",

                recipients=[
                    sub.user.email
                ]
            )

            msg.body = f"""
                Salut!

                Abonamentul "{sub.name}"
                este programat să se încheie mâine.

                Subscription Tracker
                """

            mail.send(msg)

            print(
                f"Notificare de încetare trimisă către "
                f"{sub.user.email}"
            )