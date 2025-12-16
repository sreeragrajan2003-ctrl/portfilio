from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, SectionHead, SectionBody, Enquiry,Resume


viewer_bp = Blueprint("viewer", __name__)


# ================================
# HOME PAGE / VIEWER SIDE
# ================================
@viewer_bp.route("/")
def index():
    portfolio_data = []

    # Load all sections in display order
    sections = SectionHead.query.order_by(SectionHead.display_order.asc()).all()
    resume = Resume.query.first()
    for sec in sections:
        # Load subsection items for this section
        items = SectionBody.query.filter_by(section_id=sec.id).order_by(SectionBody.item_order.asc()).all()

        # Convert SectionBody objects → dictionaries (safe for Jinja)
        item_list = []
        for i in items:
            item_list.append({
                "id": i.id,
                "content_key": i.content_key,
                "content_value": i.content_value,
                "group_id": i.group_id,
                "item_order": i.item_order
            })

        # Add section + its items to portfolio structure
        portfolio_data.append({
            "section": sec,
            "items": item_list
        })

    return render_template("index.html", portfolio_data=portfolio_data,resume=resume)


# ================================
# CONTACT FORM SUBMISSION
# ================================
@viewer_bp.route("/submit-enquiry", methods=["POST"])
def submit_enquiry():
    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")

    if not name or not email or not subject or not message:
        flash("Please fill in all fields.", "error")
        return redirect(url_for("viewer.index") + "#contact")

    new_enquiry = Enquiry(
        name=name,
        email=email,
        subject=subject,
        message=message
    )

    db.session.add(new_enquiry)
    db.session.commit()

    flash("Message sent successfully!", "success")
    return redirect(url_for("viewer.index") + "#contact")


