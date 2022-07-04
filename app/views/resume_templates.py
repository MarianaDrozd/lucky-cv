from flask import Blueprint, render_template, session, make_response
import pdfkit
from app.models import ResumeTemplateModel, ResumeModel
from app.views.decorators.decorators import admin_required
# from html2image import Html2Image
# from PIL import Image

resume_templates_bp = Blueprint('resume_templates', __name__)


@resume_templates_bp.route("/", methods=["GET"])
def index():
    user = session.get("user")
    return render_template("index.html", user=user)


@resume_templates_bp.route("/resume_templates/<int:id>", methods=["GET"])
def get_template(id):
    template = ResumeTemplateModel.find_by_id(id)
    if not template:
        return {"message": "Resume not found."}, 404

    return render_template("resume_templates/resume_template1.html")


@resume_templates_bp.route("/resume_templates/create")
@admin_required
def create_template():
    print(session.get("user"))
    return render_template("ok.html")


@resume_templates_bp.route("/print-pdf-file/<int:id_>", methods=["GET"])
def resume_pdf(id_):
    resume = ResumeModel.find_by_id(id_)
    rendered = render_template("resume_templates/resume_template2.html", resume=resume)
    pdf = pdfkit.from_string(rendered, False, css="app/static/template2_style.css")

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename={resume.first_name}_{resume.last_name}output.pdf"
    return response
