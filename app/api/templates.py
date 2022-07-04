from flask import Blueprint, request

from app.models import ResumeTemplateModel
from app.views.decorators.decorators import admin_required

api_templates_bp = Blueprint('api_templates', __name__)


@api_templates_bp.route("/APIv1/templates", methods=["GET"])
def get_templates():
    """
    Method for getting resume templates
    :return: resume templates
    """
    templates = ResumeTemplateModel.return_all()
    return {"templates": templates}, 200


@api_templates_bp.route("/APIv1/templates/<int:id>", methods=["GET"])
def get_resume(id):
    """
    Method for getting template by id
    :param id: template's id
    :return: template
    """
    template = ResumeTemplateModel.find_by_id(id)
    if not template:
        return {"message": "Not Found"}, 404

    return template.serialize


@api_templates_bp.route("/APIv1/templates", methods=["POST"])
@admin_required
def create_template():
    """
    Method for creating resume template
    :return: resume template
    """
    template = ResumeTemplateModel(
        name=request.json.get("name")
    )
    template.save_to_db()
    return template.serialize


@api_templates_bp.route("/APIv1/templates/<int:id>", methods=["PATCH"])
@admin_required
def update_template(id):
    """
    Method for creating resume template
    :return: resume template
    """
    template = ResumeTemplateModel.find_by_id(id)
    name = request.json.get("name")
    if name:
        template.name = name
    template.save_to_db()
    return {"message": "Updated"}


@api_templates_bp.route("/APIv1/templates/<int:id>", methods=["DELETE"])
@admin_required
def delete_template(id):
    """
    Method for deleting template by changing is_active to False
    :param id: template id
    :return: template with is_active=False
    """
    template = ResumeTemplateModel.find_by_id(id)
    template.is_active = False
    return template.serialize
