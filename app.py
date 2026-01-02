from flask import Flask
from models import db
from admin.routes import admin_bp
from viewer.routes import viewer_bp


app = Flask(__name__)
app.secret_key = "your_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(admin_bp)
app.register_blueprint(viewer_bp)



with app.app_context():
    db.create_all()
    from models import seed_admin
    seed_admin()


if __name__ == "__main__":
    app.run(debug=True)
