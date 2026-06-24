import os

MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_PORT = os.environ.get("MYSQL_PORT", "3306")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "changeme")
MYSQL_DB = os.environ.get("MYSQL_DB", "resume_screening_db")

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}

SECRET_KEY = os.environ.get("SECRET_KEY", "change_this_to_any_random_string")