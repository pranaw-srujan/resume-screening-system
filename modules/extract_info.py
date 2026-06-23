import re
import spacy
from modules.skills_list import SKILLS_DB

nlp = spacy.load("en_core_web_sm")

# Header keywords that signal the start of each section.
# Lowercase, since we compare against lowercased text.
EDUCATION_HEADERS = ["education", "educational qualification", "academic background", "qualification"]
EXPERIENCE_HEADERS = ["experience", "work experience", "internship", "employment history"]

# Headers for ALL sections we recognize, used to know when a section ENDS.
ALL_HEADERS = EDUCATION_HEADERS + EXPERIENCE_HEADERS + [
    "skills", "technical skills", "skills set", "summary", "objective",
    "certifications", "projects", "contact",
]


def extract_email(text):
    """Find the first email address in the text using regex."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_phone(text):
    """Find the first phone number in the text using regex."""
    pattern = r'(\+?\d{1,3}[\s-]?)?\d{10}|\+?\d{1,3}[\s-]?\d{4,5}[\s-]?\d{5,6}'
    match = re.search(pattern, text)
    return match.group(0).strip() if match else None


def _looks_like_name(line):
    """A line looks like a plausible name if it's short, has no
    email symbol, no digits, and isn't all uppercase (like a section header)."""
    if not line:
        return False
    if "@" in line or any(char.isdigit() for char in line):
        return False
    word_count = len(line.split())
    return 1 <= word_count <= 4


def extract_name(text):
    """
    Find the candidate's name using two strategies, prioritized:
    1. The first non-empty line, if it looks like a plausible name.
    2. Fallback: the first PERSON entity spaCy finds in the top section.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if lines and _looks_like_name(lines[0]):
        return lines[0]

    top_section = "\n".join(lines[:5])
    doc = nlp(top_section)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return None


def extract_skills(text):
    """
    Find skills by checking which entries from SKILLS_DB appear in the text.
    Matching is case-insensitive and uses word boundaries.
    """
    text_lower = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        pattern = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills


def _extract_section(text, section_headers):
    """
    Generic section extractor: scans line by line, collects lines that
    fall under one of the given section_headers, stopping when any other
    known header is reached.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    collected = []
    inside_section = False

    for line in lines:
        line_lower = line.lower().strip(":").strip()

        is_target_header = any(line_lower == h or line_lower.startswith(h) for h in section_headers)
        is_other_header = any(line_lower == h or line_lower.startswith(h) for h in ALL_HEADERS) and not is_target_header

        if is_target_header:
            inside_section = True
            continue

        if is_other_header:
            if inside_section:
                break
            continue

        if inside_section:
            collected.append(line)

    return "\n".join(collected) if collected else None


def extract_education(text):
    """Extract the education section from resume text."""
    return _extract_section(text, EDUCATION_HEADERS)


def extract_experience(text):
    """Extract the experience section from resume text."""
    return _extract_section(text, EXPERIENCE_HEADERS)