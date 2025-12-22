from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, AdminUser, SectionHead, SectionBody, Enquiry
import os
from werkzeug.utils import secure_filename
from models import Resume


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
@admin_bp.route("/dashboard")
@login_required
def dashboard():
    sections = SectionHead.query.order_by(SectionHead.display_order).all()
    resume = Resume.query.first()

    return render_template(
        "admin_dashboard.html",
        sections=sections,
        resume=resume
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
@admin_bp.route("/subsection/add", methods=["GET", "POST"])
@login_required
def add_subsection():

    sections = SectionHead.query.all()

    if request.method == "POST":

        section_id = request.form.get("section_id")

        keys = request.form.getlist("content_key[]")
        values = request.form.getlist("content_value[]")

        for key, value in zip(keys, values):
            if key.strip() and value.strip():
                item = SectionBody(
                    section_id=section_id,
                    content_key=key,
                    content_value=value
                )
                db.session.add(item)

        db.session.commit()
        flash("Subsections added successfully", "success")
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


@admin_bp.route("/enquiries")
@login_required
def enquiries():
    all_enquiries = Enquiry.query.order_by(Enquiry.id.desc()).all()
    return render_template("admin_enquiries.html", enquiries=all_enquiries)


@admin_bp.route("/enquiry/delete/<int:id>")
@login_required
def delete_enquiry(id):
    msg = Enquiry.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash("Enquiry deleted.", "success")
    return redirect(url_for("admin.enquiries"))


@admin_bp.route("/resume/upload", methods=["POST"])
@login_required
def upload_resume():
    file = request.files.get("resume")

    if not file or file.filename == "":
        flash("No file selected", "error")
        return redirect(url_for("admin.dashboard"))

    if not file.filename.lower().endswith(".pdf"):
        flash("Only PDF allowed", "error")
        return redirect(url_for("admin.dashboard"))

    upload_folder = "static/uploads/resume"
    os.makedirs(upload_folder, exist_ok=True)

    # 🔥 Delete old resume from DB + folder
    old = Resume.query.first()
    if old:
        old_path = os.path.join(upload_folder, old.filename)
        if os.path.exists(old_path):
            os.remove(old_path)
        db.session.delete(old)

    # Save new resume
    filename = secure_filename(file.filename)
    file.save(os.path.join(upload_folder, filename))

    new_resume = Resume(filename=filename)
    db.session.add(new_resume)
    db.session.commit()

    flash("Resume uploaded successfully!", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/enquiry/read/<int:id>")
@login_required
def mark_enquiry_read(id):
    enquiry = Enquiry.query.get_or_404(id)

    enquiry.is_read = True
    db.session.commit()

    flash("Enquiry marked as read", "success")
    return redirect(url_for("admin.enquiries"))


@admin_bp.route("/enquiry/read-all")
@login_required
def mark_all_enquiries_read():
    Enquiry.query.filter_by(is_read=False).update(
        {"is_read": True}
    )
    db.session.commit()

    flash("All enquiries marked as read", "success")
    return redirect(url_for("admin.enquiries"))


# ===========================
# UPDATE SECTION ORDER (DRAG & DROP)
# ===========================
@admin_bp.route("/sections/update-order", methods=["POST"])
@login_required
def update_section_order():
    """Handle drag-and-drop section reordering"""
    data = request.get_json()
    order = data.get("order", [])

    # order = ['3', '1', '2'] (section IDs in new order)
    for index, section_id in enumerate(order):
        section = SectionHead.query.get(int(section_id))
        if section:
            section.display_order = index

    db.session.commit()

    return jsonify({"status": "success"})
