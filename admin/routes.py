
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, AdminUser, SectionHead, SectionBody

# ===========================
# LOGIN REQUIRED DECORATOR
# ===========================
def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "admin_id" not in session:
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return wrapper

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

@admin_bp.route("/sections/add", methods=["GET", "POST"])
@login_required
def add_section_head():
    if request.method == "POST":
        section_name = request.form.get("section_name")
        section_title = request.form.get("section_title")
        section_description = request.form.get("section_description")

        # Check duplicate section
        if SectionHead.query.filter_by(section_name=section_name).first():
            flash("Section name already exists!", "error")
            return redirect(url_for("admin.add_section_head"))

        new_section = SectionHead(
            section_name=section_name,
            section_title=section_title,
            section_description=section_description
        )

        db.session.add(new_section)
        db.session.commit()

        flash("Section created successfully!", "success")
        return redirect(url_for("admin.view_sections"))

    return render_template("add_section_head.html")


@admin_bp.route("/subsections/add", methods=["GET", "POST"])
@login_required
def add_subsection():
    sections = SectionHead.query.order_by(SectionHead.section_title).all()

    if request.method == "POST":
        section_id = request.form.get("section_id")
        group_id = request.form.get("group_id")
        content_key = request.form.get("content_key")
        content_value = request.form.get("content_value")
        item_order = request.form.get("item_order")

        new_item = SectionBody(
            section_id=section_id,
            group_id=group_id,
            content_key=content_key,
            content_value=content_value,
            item_order=item_order
        )

        db.session.add(new_item)
        db.session.commit()

        flash("Subsection item added!", "success")
        return redirect(url_for("admin.add_subsection"))

    return render_template("add_subsection.html", sections=sections)

