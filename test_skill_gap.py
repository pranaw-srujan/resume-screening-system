from modules.db import get_candidates_with_combined_text, get_job_description
from modules.skill_gap import get_required_skills, get_skill_gap

jd = get_job_description(1)
required_skills = get_required_skills(jd['description_text'])

print(f"Job: {jd['title']}")
print(f"Required skills detected: {sorted(required_skills)}\n")

candidates = get_candidates_with_combined_text()

for candidate in candidates:
    candidate_skills = candidate['skills'].split(", ") if candidate['skills'] else []
    gap_result = get_skill_gap(candidate_skills, required_skills)

    print(f"--- {candidate['name']} ---")
    print(f"Matched skills: {gap_result['matched_skills']}")
    print(f"Missing skills: {gap_result['missing_skills']}")
    print(f"Match percentage: {gap_result['match_percentage']}%\n")