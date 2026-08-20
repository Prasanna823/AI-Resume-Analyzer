def get_suggestions(
    text,
    missing_skills=None
):

    text_lower = text.lower()

    suggestions = []

    if missing_skills is None:

        missing_skills = []

    # --------------------------------
    # SKILLS
    # --------------------------------

    if "skills" not in text_lower:

        suggestions.append(
            "Add a dedicated Technical Skills section."
        )

    # --------------------------------
    # PROJECTS
    # --------------------------------

    if "projects" not in text_lower:

        suggestions.append(
            "Add 2-3 relevant projects with technologies used and measurable results."
        )

    # --------------------------------
    # EXPERIENCE
    # --------------------------------

    if (
        "experience" not in text_lower
        and
        "internship" not in text_lower
    ):

        suggestions.append(
            "Add internship, training, freelance or relevant practical experience."
        )

    # --------------------------------
    # EDUCATION
    # --------------------------------

    if "education" not in text_lower:

        suggestions.append(
            "Add a clear Education section with degree, college and graduation year."
        )

    # --------------------------------
    # CERTIFICATIONS
    # --------------------------------

    if "certification" not in text_lower:

        suggestions.append(
            "Add relevant certifications or online courses."
        )

    # --------------------------------
    # GITHUB
    # --------------------------------

    if "github" not in text_lower:

        suggestions.append(
            "Add your GitHub profile to showcase your projects and code."
        )

    # --------------------------------
    # LINKEDIN
    # --------------------------------

    if "linkedin" not in text_lower:

        suggestions.append(
            "Add your LinkedIn profile to improve your professional presence."
        )

    # --------------------------------
    # ACTION WORDS
    # --------------------------------

    action_words = [
        "developed",
        "created",
        "designed",
        "implemented",
        "built",
        "improved"
    ]

    if not any(
        word in text_lower
        for word in action_words
    ):

        suggestions.append(
            "Use strong action words such as Developed, Designed, Built and Implemented."
        )

    # --------------------------------
    # MISSING JOB SKILLS
    # --------------------------------

    if missing_skills:

        skills_text = ", ".join(
            missing_skills[:5]
        )

        suggestions.append(
            f"For the selected role, consider learning or adding these skills: {skills_text}."
        )

    # --------------------------------
    # DEFAULT
    # --------------------------------

    if not suggestions:

        suggestions.append(
            "Your resume has a strong basic structure. Continue adding measurable achievements."
        )

    return suggestions