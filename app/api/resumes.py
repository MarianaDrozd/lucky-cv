from flask import Blueprint, request, session

from app.models import ResumeModel
from app.views.decorators.decorators import login_required

api_resumes_bp = Blueprint("api_resumes", __name__)

RESUME_FIELDS = ['title', 'first_name', 'last_name', 'email', 'phone_number', 'linkedin', 'github', 'location',
                 'summary', 'education', 'job_experience', 'hard_skills', 'soft_skills', 'languages']


# TODO: fix api methods!!!!!!!!!!!!!!!!!!!!!!

@api_resumes_bp.route("/APIv1/resumes", methods=["GET"])
@login_required
def get_resumes():
    """
    Method for getting all resumes by authorized user
    :return: user, resumes
    """
    user = session.get("user")
    resumes = ResumeModel.find_by_user_id(user.get("id"))
    return {"user": user, "resumes": resumes}


@api_resumes_bp.route("/APIv1/resumes/<int:id_>", methods=["GET"])
def get_resume(id_):
    """
    Method for getting resume by id
    :param id_: resume's id
    :return: resume
    """
    resume = ResumeModel.find_by_id(id_)
    if not resume:
        return {"message": "Not Found"}, 404

    return resume.serialize()


@api_resumes_bp.route("/APIv1/resumes", methods=["POST"])
@login_required
def create_resume():
    """
    Method for creating resume.
    :return: resume
    """
    if not request.json:
        return {"message": "Please, specify 'title', 'first_name', 'last_name', 'email', 'phone_number', 'linkedin', "
                           "'github', 'location', 'summary', 'education', 'job_experience', 'hard_skills', 'soft_skills',"
                           "'languages'"}
    user = session.get("user")
    resume = ResumeModel(
        user_id=user.get("id"),
        title=request.json.get("title"),
        first_name=request.json.get("first_name"),
        last_name=request.json.get("last_name"),
        email=request.json.get("email"),
        phone_number=request.json.get("phone_number"),
        linkedin=request.json.get("linkedin"),
        github=request.json.get("github"),
        location=request.json.get("location"),
        summary=request.json.get("summary"),
        education=request.json.get("education"),
        job_experience=request.json.get("job_experience"),
        hard_skills=request.json.get("hard_skills"),
        soft_skills=request.json.get("soft_skills"),
        languages=request.json.get("languages")
    )
    resume.save_to_db()
    return resume.serialize, 201


@api_resumes_bp.route("/APIv1/resumes/<int:id>/", methods=["PATCH"])
@login_required
def update_resume(id_):
    """
    Method for updating resume
    :param id_: resume id
    :return: message
    """
    user = session.get("user")
    resume = ResumeModel.find_by_id(id_)
    if resume and user.get("id") == resume.serialize["user_id"]:
        for field in RESUME_FIELDS:
            field = request.json.get(f"{field}")
            if field:
                resume.field = field
        resume.save_to_db()

        return {"message": "Updated"}
    return {"message": "Resume Not Found or belongs to Another User"}


@api_resumes_bp.route("/APIv1/resumes/<int:id>", methods=["DELETE"])
def delete_resume(id_):
    """
    Method for deleting resume
    :param id_: resume id
    :return: deleted resume with is_active=False
    """
    resume = ResumeModel.find_by_id(id_)
    resume.is_active = False
    resume.save_to_db()
    if not resume:
        return {"Resume Not Found"}, 404

    return resume.serialize
