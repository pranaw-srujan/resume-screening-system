import mysql.connector
import config


def get_connection():
    """Create and return a new MySQL database connection."""
    return mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB
    )


def save_candidate(name, email, phone, skills, education, experience):
    """Insert a new candidate record into the candidates table."""
    conn = get_connection()
    cursor = conn.cursor()

    skills_str = ", ".join(skills) if skills else ""

    query = """
        INSERT INTO candidates (name, email, phone, skills, education, experience)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, email, phone, skills_str, education, experience))
    conn.commit()

    candidate_id = cursor.lastrowid

    cursor.close()
    conn.close()
    return candidate_id


def save_job_description(title, description_text, required_skills=""):
    """Insert a new job description record."""
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO job_descriptions (title, description_text, required_skills)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (title, description_text, required_skills))
    conn.commit()

    jd_id = cursor.lastrowid

    cursor.close()
    conn.close()
    return jd_id


def get_all_candidates():
    """Fetch all candidates from the database."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM candidates")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_job_description(jd_id):
    """Fetch a single job description by its ID."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM job_descriptions WHERE jd_id = %s", (jd_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result
def get_candidates_with_combined_text():
    """
    Fetch all candidates and build a combined 'resume_text' field for each,
    merging skills, education, and experience into one block of text
    suitable for TF-IDF comparison.
    """
    candidates = get_all_candidates()

    for candidate in candidates:
        combined = " ".join([
            candidate.get("skills") or "",
            candidate.get("education") or "",
            candidate.get("experience") or "",
        ])
        candidate["resume_text"] = combined

    return candidates