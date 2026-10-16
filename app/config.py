import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-me")
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{os.path.join(PROJECT_ROOT, 'student_management.db')}")
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_TIME_LIMIT = 3600
