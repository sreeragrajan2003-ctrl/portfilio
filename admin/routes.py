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

# ===========================
# LOGIN
# ===========================
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

    return render_template("admin_login.html")


# ===========================
# DASHBOARD (SHOW SECTIONS + SUBSECTIONS)
# ===========================
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    # ✅ Order section by display_order
    sections = SectionHead.query.order_by(SectionHead.display_order.asc()).all()

    return render_template(
        "admin_dashboard.html",
        sections=sections
    )



# ===========================
# LOGOUT
# ===========================
@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("admin.login"))


# ===========================
# ADD SECTION HEAD
# ===========================
@admin_bp.route("/sections/add", methods=["GET", "POST"])
@login_required
def add_section_head():
    if request.method == "POST":
        section_name = request.form.get("section_name")
        section_title = request.form.get("section_title")
        section_description = request.form.get("section_description")
        display_order = request.form.get("display_order", 0)

        if SectionHead.query.filter_by(section_name=section_name).first():
            flash("Section already exists!", "error")
            return redirect(url_for("admin.add_section_head"))

        new_section = SectionHead(
            section_name=section_name,
            section_title=section_title,
            section_description=section_description,
            display_order=display_order
        )

        db.session.add(new_section)
        db.session.commit()

        flash("Section added successfully!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("add_section_head.html")


# ===========================
# ADD SUBSECTION
# ===========================
@admin_bp.route("/subsections/add", methods=["GET", "POST"])
@login_required
def add_subsection():
    sections = SectionHead.query.order_by(SectionHead.display_order).all()

    if request.method == "POST":
        section_id = request.form.get("section_id")
        content_key = request.form.get("content_key")
        content_value = request.form.get("content_value")
        group_id = request.form.get("group_id", 0)
        item_order = request.form.get("item_order", 0)

        if not content_key or not content_value:
            flash("All fields are required!", "error")
            return redirect(url_for("admin.add_subsection"))

        new_item = SectionBody(
            section_id=section_id,
            content_key=content_key,
            content_value=content_value,
            group_id=group_id,
            item_order=item_order
        )

        db.session.add(new_item)
        db.session.commit()

        flash("Subsection added successfully!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("add_subsection.html", sections=sections)

#  Delete section 
@admin_bp.route("/sections/delete/<int:id>")
@login_required
def delete_section(id):
    section = SectionHead.query.get_or_404(id)
    db.session.delete(section)
    db.session.commit()
    flash("Section deleted successfully!", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/sections/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_section(id):
    section = SectionHead.query.get_or_404(id)

    if request.method == "POST":
        section.section_name = request.form.get("section_name")
        section.section_title = request.form.get("section_title")
        section.section_description = request.form.get("section_description")
        section.display_order = request.form.get("display_order")
        db.session.commit()

        flash("Section updated successfully!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("edit_section.html", section=section)


@admin_bp.route("/subsections/delete/<int:id>")
@login_required
def delete_subsection(id):
    item = SectionBody.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash("Subsection deleted", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/subsections/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_subsection(id):
    item = SectionBody.query.get_or_404(id)

    if request.method == "POST":
        item.content_key = request.form.get("content_key")
        item.content_value = request.form.get("content_value")
        item.item_order = request.form.get("item_order")
        db.session.commit()

        flash("Subsection updated!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("edit_subsection.html", item=item)
