from modules.extract_info import extract_skills


def get_required_skills(job_description_text):
    """
    Extract the set of required skills from a job description's text,
    reusing the same skill-matching logic used for resumes.
    """
    return set(extract_skills(job_description_text))


def get_skill_gap(candidate_skills, required_skills):
    """
    Given a candidate's skills and a job's required skills (both as
    lists or sets), return the skills the candidate is missing.
    """
    candidate_set = set(s.strip().lower() for s in candidate_skills) if candidate_skills else set()
    required_set = set(s.strip().lower() for s in required_skills) if required_skills else set()

    missing = required_set - candidate_set
    matched = required_set & candidate_set

    return {
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "match_percentage": round((len(matched) / len(required_set) * 100), 1) if required_set else 0.0
    }