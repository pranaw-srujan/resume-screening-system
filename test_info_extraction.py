from modules.extract_text import extract_text
from modules.extract_info import (
    extract_email, extract_phone, extract_name,
    extract_skills, extract_education, extract_experience
)

resumes = [
    "static/uploads/sample_resume_1_aditi.docx",
    "static/uploads/sample_resume_2_rohit.docx",
    "static/uploads/sample_resume_3_sneha.docx",
]

for filepath in resumes:
    text = extract_text(filepath)
    print(f"=== {filepath} ===")
    print("Name:", extract_name(text))
    print("Email:", extract_email(text))
    print("Phone:", extract_phone(text))
    print("Skills:", extract_skills(text))
    print("Education:\n", extract_education(text))
    print("Experience:\n", extract_experience(text))
    print()