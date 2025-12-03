from flask import Flask, render_template, request, redirect, url_for, flash
from message import db, Enquiry

app = Flask(__name__)
app.secret_key = "hello"

# -----------------------------
# DATABASE CONFIG (MUST COME BEFORE init_app)
# -----------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///enquiries.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# -----------------------------
# INITIALIZE DATABASE
# -----------------------------
db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

# -----------------------------
# SAVE ENQUIRY ROUTE
# -----------------------------
@app.route('/submit-enquiry', methods=['POST'])
def submit_enquiry():
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")

    new_msg = Enquiry(email=email, subject=subject, message=message)
    db.session.add(new_msg)
    db.session.commit()

    flash("Your enquiry has been saved!", "success")
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
