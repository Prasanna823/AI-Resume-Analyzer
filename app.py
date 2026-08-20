from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import re

from parser.resume_parser import extract_text
from models.skills import skills_list
from ats.ats_score import calculate_score
from suggestions.suggestions import get_suggestions
from database.db import (
    init_database,
    create_user,
    get_user_by_email,
    save_analysis,
    get_user_analyses
)


app = Flask(__name__)

app.secret_key = "ai_resume_analyzer_secret_key_change_this"

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --------------------------------------------------
# JOB ROLES
# --------------------------------------------------

ROLES = [
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Python Developer",
    "Java Developer",
    "AI Engineer",
    "Machine Learning Engineer",
    "Data Analyst",
    "Data Scientist",
    "UI/UX Designer",
    "Cloud Engineer",
    "Cybersecurity Analyst",
    "DevOps Engineer",
    "Software Tester",
    "Mobile App Developer"
]


# --------------------------------------------------
# REQUIRED SKILLS FOR EACH JOB
# --------------------------------------------------

ROLE_SKILLS = {

    "Frontend Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Bootstrap",
        "Git"
    ],

    "Backend Developer": [
        "Python",
        "Flask",
        "SQL",
        "API",
        "Git"
    ],

    "Full Stack Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Python",
        "Flask",
        "SQL",
        "Git"
    ],

    "Python Developer": [
        "Python",
        "Flask",
        "Django",
        "SQL",
        "Git"
    ],

    "Java Developer": [
        "Java",
        "Spring Boot",
        "SQL",
        "Git"
    ],

    "AI Engineer": [
        "Python",
        "Artificial Intelligence",
        "Machine Learning",
        "Deep Learning",
        "NLP"
    ],

    "Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "Scikit-learn",
        "TensorFlow",
        "Deep Learning"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Data Analysis"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Machine Learning",
        "Pandas",
        "Data Analysis"
    ],

    "UI/UX Designer": [
        "Figma",
        "Canva",
        "UI/UX Design",
        "User Research"
    ],

    "Cloud Engineer": [
        "AWS",
        "Azure",
        "Docker",
        "Kubernetes",
        "Linux"
    ],

    "Cybersecurity Analyst": [
        "Cyber Security",
        "Network Security",
        "Ethical Hacking",
        "Linux"
    ],

    "DevOps Engineer": [
        "Docker",
        "Kubernetes",
        "AWS",
        "CI/CD",
        "Git"
    ],

    "Software Tester": [
        "Software Testing",
        "Selenium",
        "Python",
        "SQL",
        "API"
    ],

    "Mobile App Developer": [
        "Flutter",
        "React Native",
        "Android Development",
        "Java",
        "Git"
    ]
}


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/")
def home():

    return render_template(
        "index.html",
        logged_in="user_id" in session
    )


# --------------------------------------------------
# SIGNUP
# --------------------------------------------------

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not password:

            flash("Please fill all fields.", "error")

            return redirect(url_for("signup"))

        if password != confirm_password:

            flash("Passwords do not match.", "error")

            return redirect(url_for("signup"))

        if len(password) < 6:

            flash("Password must contain at least 6 characters.", "error")

            return redirect(url_for("signup"))

        existing_user = get_user_by_email(email)

        if existing_user:

            flash("An account with this email already exists.", "error")

            return redirect(url_for("login"))

        password_hash = generate_password_hash(password)

        user_id = create_user(
            name,
            email,
            password_hash
        )

        session["user_id"] = user_id
        session["user_name"] = name

        flash("Account created successfully!", "success")

        return redirect(url_for("dashboard"))

    return render_template("signup.html")


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = get_user_by_email(email)

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            flash("Login successful!", "success")

            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

@app.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "success")

    return redirect(url_for("home"))


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(url_for("login"))

    analyses = get_user_analyses(
        session["user_id"]
    )

    return render_template(
        "dashboard.html",
        roles=ROLES,
        analyses=analyses,
        user_name=session.get("user_name", "User")
    )


# --------------------------------------------------
# UPLOAD PAGE
# --------------------------------------------------

@app.route("/upload")
def upload():

    if "user_id" not in session:

        return redirect(url_for("login"))

    return render_template(
        "upload.html",
        roles=ROLES
    )


# --------------------------------------------------
# ANALYZE RESUME
# --------------------------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    # -----------------------------------------
    # CHECK LOGIN
    # -----------------------------------------

    if "user_id" not in session:

        flash(
            "Please login before analyzing a resume.",
            "error"
        )

        return redirect(url_for("login"))


    # -----------------------------------------
    # GET FORM DATA
    # -----------------------------------------

    role = request.form.get("role", "").strip()

    resume = request.files.get("resume")


    # -----------------------------------------
    # CHECK JOB ROLE
    # -----------------------------------------

    if not role:

        flash(
            "Please select a job role.",
            "error"
        )

        return redirect(url_for("dashboard"))


    # -----------------------------------------
    # CHECK FILE
    # -----------------------------------------

    if resume is None:

        flash(
            "No resume was uploaded.",
            "error"
        )

        return redirect(url_for("dashboard"))


    if resume.filename == "":

        flash(
            "Please select a resume PDF.",
            "error"
        )

        return redirect(url_for("dashboard"))


    # -----------------------------------------
    # CHECK PDF
    # -----------------------------------------

    if not resume.filename.lower().endswith(".pdf"):

        flash(
            "Only PDF files are supported.",
            "error"
        )

        return redirect(url_for("dashboard"))


    # -----------------------------------------
    # CREATE SAFE UNIQUE FILENAME
    # -----------------------------------------

    import uuid

    original_name = secure_filename(
        resume.filename
    )

    unique_name = (
        str(uuid.uuid4())
        + "_"
        + original_name
    )


    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_name
    )


    # -----------------------------------------
    # SAVE FILE
    # -----------------------------------------

    try:

        resume.save(filepath)

    except Exception as error:

        print(
            "UPLOAD ERROR:",
            error
        )

        flash(
            "Could not save the uploaded resume.",
            "error"
        )

        return redirect(url_for("dashboard"))


    # -----------------------------------------
    # EXTRACT TEXT
    # -----------------------------------------

    try:

        text = extract_text(filepath)

    except Exception as error:

        print(
            "PDF EXTRACTION ERROR:",
            error
        )

        flash(
            "Unable to read this PDF. Please try another PDF.",
            "error"
        )

        return redirect(url_for("dashboard"))


    # -----------------------------------------
    # CHECK EXTRACTED TEXT
    # -----------------------------------------

    if not text or len(text.strip()) < 20:

        flash(
            "No readable text was found in the PDF. Please upload a text-based resume PDF.",
            "error"
        )

        return redirect(url_for("dashboard"))


    # -----------------------------------------
    # NORMALIZE TEXT
    # -----------------------------------------

    text_lower = text.lower()


    # -----------------------------------------
    # DETECT SKILLS
    # -----------------------------------------

    detected_skills = []

    for skill in skills_list:

        skill_lower = skill.lower()

        pattern = r"\b" + re.escape(
            skill_lower
        ) + r"\b"

        if re.search(
            pattern,
            text_lower
        ):

            detected_skills.append(skill)


    # Remove duplicates

    detected_skills = list(
        dict.fromkeys(
            detected_skills
        )
    )


    # -----------------------------------------
    # ATS SCORE
    # -----------------------------------------

    try:

        ats_score = calculate_score(
            text
        )

    except Exception as error:

        print(
            "ATS ERROR:",
            error
        )

        ats_score = 0


    # -----------------------------------------
    # REQUIRED SKILLS
    # -----------------------------------------

    required_skills = ROLE_SKILLS.get(
        role,
        []
    )


    # -----------------------------------------
    # MATCHED / MISSING SKILLS
    # -----------------------------------------

    matched_skills = []

    missing_skills = []

    detected_lower = [
        skill.lower()
        for skill in detected_skills
    ]


    for skill in required_skills:

        if skill.lower() in detected_lower:

            matched_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )


    # -----------------------------------------
    # JOB MATCH %
    # -----------------------------------------

    if len(required_skills) > 0:

        match_percentage = int(
            (
                len(matched_skills)
                /
                len(required_skills)
            )
            * 100
        )

    else:

        match_percentage = 0


    # -----------------------------------------
    # MATCH STATUS
    # -----------------------------------------

    if match_percentage >= 80:

        match_status = "Excellent Match"

    elif match_percentage >= 60:

        match_status = "Good Match"

    elif match_percentage >= 40:

        match_status = "Partial Match"

    else:

        match_status = "Needs Improvement"


    # -----------------------------------------
    # SUGGESTIONS
    # -----------------------------------------

    try:

        suggestions = get_suggestions(
            text,
            missing_skills
        )

    except Exception as error:

        print(
            "SUGGESTION ERROR:",
            error
        )

        suggestions = [
            "Review your resume structure.",
            "Add skills relevant to your selected job role.",
            "Add measurable achievements to your projects."
        ]


    # -----------------------------------------
    # SAVE ANALYSIS TO DATABASE
    # -----------------------------------------

    try:

        save_analysis(
            session["user_id"],
            original_name,
            role,
            ats_score,
            match_percentage
        )

    except Exception as error:

        print(
            "DATABASE ERROR:",
            error
        )


    # -----------------------------------------
    # BEST MATCHING ROLE FOR THE RESUME
    # -----------------------------------------

    # Compare detected skills with all 15 job roles.
    role_matches = []

    detected_lower_set = {
        skill.lower()
        for skill in detected_skills
    }

    for job_role, job_skills in ROLE_SKILLS.items():

        if job_skills:
            role_matched_skills = [
                skill
                for skill in job_skills
                if skill.lower() in detected_lower_set
            ]

            role_score = int(
                len(role_matched_skills)
                / len(job_skills)
                * 100
            )
        else:
            role_matched_skills = []
            role_score = 0

        role_matches.append({
            "role": job_role,
            "score": role_score,
            "matched_skills": role_matched_skills
        })

    role_matches.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    best_role = (
        role_matches[0]["role"]
        if role_matches
        else "Not Available"
    )

    best_role_score = (
        role_matches[0]["score"]
        if role_matches
        else 0
    )

    top_roles = role_matches[:5]


    # -----------------------------------------
    # SHOW RESULTS
    # -----------------------------------------

    return render_template(
        "result.html",

        ats_score=ats_score,

        role=role,

        skills=detected_skills,

        missing=missing_skills,

        suggestions=suggestions,

        match=match_percentage,

        match_status=match_status,

        best_role=best_role,

        best_role_score=best_role_score,

        top_roles=top_roles
    )


# --------------------------------------------------
# ERROR: FILE TOO LARGE
# --------------------------------------------------

@app.errorhandler(413)
def file_too_large(error):

    flash(
        "Resume file is too large. Maximum size is 5 MB.",
        "error"
    )

    return redirect(url_for("dashboard"))


# --------------------------------------------------
# START APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    init_database()

    app.run(
        debug=True
    )