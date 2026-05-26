from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from apscheduler.schedulers.background import BackgroundScheduler

import os

from dotenv import load_dotenv

load_dotenv()


db = SQLAlchemy()

mail = Mail()

login_manager = LoginManager()

login_manager.login_view = "auth.login"

from .notification import check_notifications
def create_app():
    
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        os.getenv("DATABASE_URL")
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
    app.config["MAIL_SERVER"] = "smtp.gmail.com"

    app.config["MAIL_PORT"] = 587

    app.config["MAIL_USE_TLS"] = True

    app.config["MAIL_USERNAME"] = (
        os.getenv("MAIL_USERNAME")
    )

    app.config["MAIL_PASSWORD"] = (
        os.getenv("MAIL_PASSWORD")
    )

    app.config["MAIL_DEFAULT_SENDER"] = (
    os.getenv("MAIL_USERNAME")
    )
    db.init_app(app)

    mail.init_app(app)

    scheduler = BackgroundScheduler()

    scheduler.add_job(
    func=lambda: run_notifications(app),
    trigger='cron',
    hour=0,
    minute=0
    )

    scheduler.start()


    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(
            int(user_id)
        )

    from .routes.auth import auth
    from .routes.home import homes

    app.register_blueprint(auth)

    app.register_blueprint(homes)

    with app.app_context():

        db.create_all()

    return app
def run_notifications(app):

    with app.app_context():

        check_notifications()