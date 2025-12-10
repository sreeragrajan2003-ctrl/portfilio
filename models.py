from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ===========================
# ADMIN USER MODEL
# ===========================
class AdminUser(db.Model):
    __tablename__ = "admin_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# ===========================
# SECTION HEAD TABLE
# ===========================
class SectionHead(db.Model):
    __tablename__ = "section_head"

    id = db.Column(db.Integer, primary_key=True)
    section_name = db.Column(db.String(100), unique=True, nullable=False)
    section_title = db.Column(db.String(200), nullable=False)
    section_description = db.Column(db.Text)
    display_order = db.Column(db.Integer, default=0)

    items = db.relationship("SectionBody", backref="section", cascade="all, delete",
                            order_by="SectionBody.item_order")


# ===========================
# SECTION BODY TABLE
# ===========================
class SectionBody(db.Model):
    __tablename__ = "section_body"

    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey("section_head.id"), nullable=False)

    content_key = db.Column(db.String(100), nullable=False)
    content_value = db.Column(db.Text, nullable=False)

    group_id = db.Column(db.Integer, default=0)
    item_order = db.Column(db.Integer, default=0)
