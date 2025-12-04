from flask import Blueprint, render_template, request, redirect, url_for, session,flash
from models import AdminUser, db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin = AdminUser.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            session["admin_id"] = admin.id
            session["admin_username"] = admin.username
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for("admin.login"))

    return render_template("admin_login.html")


@admin_bp.route('/dashboard')
def dashboard():
    if "admin_id" not in session:
        return redirect(url_for("admin.login"))
    return render_template("admin_dashboard.html")

@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("admin.login"))