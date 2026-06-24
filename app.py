os.makedirs('static/uploads', exist_ok=True)
from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from modules.extract_text import extract_text
from modules.extract_info import (
    extract_email, extract_phone, extract_name,
    extract_skills, extract_education, extract_experience
)
from modules.db import (
    save_candidate, save_job_description,
    get_candidates_with_combined_text, get_job_description, get_connection
)
from modules.matcher import rank_candidates
from modules.skill_gap import get_required_skills, get_skill_gap

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """Check that the file has an allowed extension (pdf or docx)."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    message = None
    candidate_data = None

    if request.method == 'POST':
        if 'resume' not in request.files:
            message = "No file part in the request."
            return render_template('upload.html', message=message)

        file = request.files['resume']

        if file.filename == '':
            message = "No file selected."
            return render_template('upload.html', message=message)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                text = extract_text(filepath)

                candidate_data = {
                    "name": extract_name(text),
                    "email": extract_email(text),
                    "phone": extract_phone(text),
                    "skills": extract_skills(text),
                    "education": extract_education(text),
                    "experience": extract_experience(text),
                }

                save_candidate(
                    candidate_data["name"],
                    candidate_data["email"],
                    candidate_data["phone"],
                    candidate_data["skills"],
                    candidate_data["education"],
                    candidate_data["experience"],
                )

                message = f"File '{filename}' uploaded and candidate data saved successfully!"

            except Exception as e:
                message = f"File uploaded, but processing failed: {e}"
        else:
            message = "Invalid file type. Only PDF and DOCX are allowed."

    return render_template('upload.html', message=message, candidate_data=candidate_data)


@app.route('/job-description', methods=['GET', 'POST'])
def job_description():
    message = None

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        try:
            jd_id = save_job_description(title, description)
            message = f"Job description '{title}' saved successfully! (ID: {jd_id})"
        except Exception as e:
            message = f"Failed to save job description: {e}"

    return render_template('job_description.html', message=message)


def get_all_job_descriptions():
    """Fetch all job descriptions for the dropdown selector on the dashboard."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT jd_id, title FROM job_descriptions ORDER BY jd_id DESC")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    all_jds = get_all_job_descriptions()
    ranked_candidates = None
    selected_jd = None

    selected_jd_id = request.form.get('jd_id') if request.method == 'POST' else request.args.get('jd_id')

    if selected_jd_id:
        selected_jd = get_job_description(int(selected_jd_id))
        candidates = get_candidates_with_combined_text()

        ranked_candidates = rank_candidates(candidates, selected_jd['description_text'])

        required_skills = get_required_skills(selected_jd['description_text'])

        for candidate in ranked_candidates:
            candidate_skills = candidate['skills'].split(", ") if candidate['skills'] else []
            gap_result = get_skill_gap(candidate_skills, required_skills)
            candidate['matched_skills'] = gap_result['matched_skills']
            candidate['missing_skills'] = gap_result['missing_skills']
            candidate['skill_match_percentage'] = gap_result['match_percentage']

    return render_template(
        'dashboard.html',
        all_jds=all_jds,
        ranked_candidates=ranked_candidates,
        selected_jd=selected_jd
    )


if __name__ == '__main__':
    app.run(debug=True)