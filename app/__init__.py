from flask import Flask

from .models import db
from .routes import main
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config")

    db.init_app(app)
    csrf.init_app(app)
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        seed_default_data()

    return app


def seed_default_data():
    from .models import Course, Department

    if Department.query.count() == 0:
        departments = [
            Department(name="Computer Science"),
            Department(name="Business Administration"),
            Department(name="Engineering"),
            Department(name="Arts & Humanities"),
        ]
        db.session.add_all(departments)
        db.session.commit()

    if Course.query.count() == 0:
        dept_lookup = {dept.name: dept for dept in Department.query.all()}
        courses = {
            "Computer Science": ["Python Programming", "Database Systems", "Web Development"],
            "Business Administration": ["Marketing", "Finance", "Management"],
            "Engineering": ["Mechanical Design", "Electrical Circuits", "Thermodynamics"],
            "Arts & Humanities": ["Literature", "History", "Philosophy"],
        }

        records = []
        for dept_name, names in courses.items():
            department = dept_lookup[dept_name]
            for name in names:
                records.append(Course(name=name, department=department))

        db.session.add_all(records)
        db.session.commit()
