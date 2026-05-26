from app import create_app
from app.notification import check_notifications

app = create_app()

with app.app_context():
    check_notifications()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)