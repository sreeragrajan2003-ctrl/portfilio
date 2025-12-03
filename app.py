from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from message import db, Enquiry, Admin

app = Flask(__name__)
app.secret_key = "hello"

# DATABASE CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///enquiries.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# ===========================
# HOME PAGE (Viewer + Admin)
# ===========================
@app.route('/')
def home():
    messages = None

    # If admin is logged in -> show messages
    if session.get("admin"):
        messages = Enquiry.query.all()

    return render_template("index.html", messages=messages)

# ===========================
# SUBMIT ENQUIRY (Viewer)
# ===========================
@app.route('/submit-enquiry', methods=['POST'])
def submit_enquiry():
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")

    new_msg = Enquiry(email=email, subject=subject, message=message)
    db.session.add(new_msg)
    db.session.commit()

    flash("Enquiry Submitted!", "success")
    return redirect(url_for('home'))

# ===========================
# ADMIN LOGIN
# ===========================
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            session["admin"] = True
            return redirect(url_for("home"))
        else:
            flash("Invalid login!", "danger")

    return render_template("admin_login.html")

# ===========================
# ADMIN LOGOUT
# ===========================
@app.route('/admin/logout')
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("home"))

# ===========================
# DATABASE CREATE + DEFAULT ADMIN
# ===========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Create admin if not exist
        if not Admin.query.filter_by(username="admin").first():
            admin = Admin(
                username="admin",
                password=generate_password_hash("1234")
            )
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)
