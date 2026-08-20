def calculate_score(text):

    text = text.lower()

    score = 0

    # --------------------------------
    # RESUME SECTIONS
    # --------------------------------

    if "skills" in text:
        score += 15

    if "projects" in text:
        score += 15

    if "education" in text:
        score += 10

    if "experience" in text:
        score += 15

    if "internship" in text:
        score += 10

    if "certification" in text:
        score += 10

    # --------------------------------
    # PROFESSIONAL LINKS
    # --------------------------------

    if "github" in text:
        score += 5

    if "linkedin" in text:
        score += 5

    # --------------------------------
    # CONTACT INFORMATION
    # --------------------------------

    if "@" in text:
        score += 5

    phone_pattern = r"\b\d{10}\b"

    import re

    if re.search(phone_pattern, text):
        score += 5

    # --------------------------------
    # LIMIT SCORE
    # --------------------------------

    if score > 100:

        score = 100

    return score