from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match_score(resume_text, job_description_text):
    """
    Calculate a similarity score between a resume and a job description
    using TF-IDF vectorization and cosine similarity.

    Returns a float between 0 and 1, where 1 means a perfect textual match.
    """
    documents = [job_description_text, resume_text]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    score = similarity_matrix[0][0]
    return round(float(score), 4)


def rank_candidates(candidates, job_description_text):
    """
    Given a list of candidate dicts (each with 'resume_text' and other fields)
    and a job description, return the same list with a 'match_score' added
    to each candidate, sorted highest score first.
    """
    for candidate in candidates:
        resume_text = candidate.get('resume_text', '')
        candidate['match_score'] = calculate_match_score(resume_text, job_description_text)

    ranked = sorted(candidates, key=lambda c: c['match_score'], reverse=True)
    return ranked