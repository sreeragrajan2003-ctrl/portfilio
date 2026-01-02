from flask import Flask
from models import db
from admin.routes import admin_bp
from viewer.routes import viewer_bp
from werkzeug.security import generate_password_hash




app = Flask(__name__)
app.secret_key = "your_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(admin_bp)
app.register_blueprint(viewer_bp)
def seed_admin():
    from app import db
    from models import Admin

    # check if admin already exists
    existing_admin = Admin.query.filter_by(username="Sreerag").first()
    if existing_admin:
        return

    admin = Admin(
        username="Sreerag",
        password=generate_password_hash("Radhika@123")
    )

    db.session.add(admin)
    db.session.commit()

    print("Seeded default admin")


with app.app_context():
    db.create_all()

    seed_admin()


if __name__ == "__main__":
    app.run(debug=True)
