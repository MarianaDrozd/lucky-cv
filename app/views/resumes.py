from flask import request, Blueprint, session, render_template, redirect

from app.database.database import db
from app.models import ResumeModel
from app.views.decorators.decorators import login_required

resumes_bp = Blueprint('resumes', __name__)

RESUME_FIELDS = ['title', 'first_name', 'last_name', 'email', 'phone_number', 'linkedin', 'github', 'location',
                 'summary', 'education', 'job_experience', 'hard_skills', 'soft_skills', 'languages']


@resumes_bp.route("/resumes", methods=["GET"])
@login_required
def get_resumes():
    """
        Method for getting all resumes by authorized user
    """
    user = session.get("user")
    resumes = ResumeModel.find_by_user_id(user.get("id"))
    return render_template("resumes/resumes.html", resumes=resumes, user=user)


@resumes_bp.route("/resumes/<int:id>", methods=["GET"])
def get_resume(id_):
    """
    Method for getting resume by id
    :param id_: resume's id
    :return: resume
    """
    resume = ResumeModel.find_by_id(id_)
    if not resume:
        return render_template("errors/error_404.html")

    return render_template("resumes/resume.html", resume=resume)


@resumes_bp.route("/create-resume", methods=["GET", "POST"])
@login_required
def create_resume():
    """
    Method for saving resume data
    """
    if request.method == "POST":
        user = session.get("user")
        resume = ResumeModel(
            user_id=user.get("id"),
            title=request.form.get("title"),
            first_name=request.form.get("first_name"),
            last_name=request.form.get("last_name"),
            email=request.form.get("email"),
            phone_number=request.form.get("phone_number"),
            linkedin=request.form.get("linkedin"),
            github=request.form.get("github"),
            location=request.form.get("location"),
            summary=request.form.get("summary"),
            education=request.form.get("education"),
            job_experience=request.form.get("job_experience"),
            hard_skills=request.form.get("hard_skills"),
            soft_skills=request.form.get("soft_skills"),
            languages=request.form.get("languages")
        )

        resume.save_to_db()
        return redirect("/resumes")
    else:
        user = session.get("user")
        if user["activated"]:
            return render_template("resumes/create_resume.html", user=user)
        return render_template("errors/need_activation.html")


@resumes_bp.route("/resumes/update/<int:id_>", methods=["GET", "POST"])
def update_resume(id_):
    """
    Method to update resume
    :param id_ - resume's id
    """

    resume = ResumeModel.find_by_id(id_)
    if request.method == "POST":
        if resume:
            resume.delete_from_db()
            for i in RESUME_FIELDS:
                resume[i] = request.form.get(i)
            resume = ResumeModel(id_=id_)
            resume.save_to_db()

    return redirect("/")


@resumes_bp.route("/resumes/<int:id_>/delete", methods=["GET", "POST"])
@login_required
def delete_resume(id_):
    """
    Method for deleting resume
    :param id_: resume id
    """
    resume = ResumeModel.find_by_id(id_)
    resume.is_active = False
    resume.save_to_db()
    if not resume:
        return render_template("errors/error_404.html"), 404

    return redirect("/")


@resumes_bp.route("/resumes/<int:id_>/print")
def print_resume(id_):
    resume = ResumeModel.find_by_id(id_)
    return render_template("resume_templates/resume_template2.html", resume=resume)
