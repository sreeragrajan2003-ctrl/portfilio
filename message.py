from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Enquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
