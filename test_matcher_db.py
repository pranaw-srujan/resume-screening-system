from modules.db import get_candidates_with_combined_text, get_job_description
from modules.matcher import rank_candidates

jd = get_job_description(1)  # using job description with jd_id = 1
candidates = get_candidates_with_combined_text()

ranked = rank_candidates(candidates, jd['description_text'])

print(f"Job Description: {jd['title']}\n")
for rank, candidate in enumerate(ranked, start=1):
    print(f"#{rank} - {candidate['name']} - Score: {candidate['match_score']}")