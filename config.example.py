# ============================================
# Configuration TEMPLATE for the Resume Screening System
# Copy this file to config.py and fill in your real values.
# config.py is excluded from Git via .gitignore (it contains secrets).
# ============================================

import os

# MySQL Database Configuration
# For local development, fill these in directly.
# For deployment (Render), these are read from environment variables instead.
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "YOUR_MYSQL_PASSWORD_HERE")
MYSQL_DB = os.environ.get("MYSQL_DB", "resume_screening_db")

# File Upload Configuration
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}

# Flask App Secret Key
SECRET_KEY = os.environ.get("SECRET_KEY", "change_this_to_any_random_string")
