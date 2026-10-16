from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    courses = db.relationship("Course", back_populates="department", cascade="all, delete-orphan")
    students = db.relationship("Student", back_populates="department")


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    department = db.relationship("Department", back_populates="courses")
    students = db.relationship("Student", back_populates="course")
    academic_records = db.relationship("AcademicRecord", back_populates="course")


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    department = db.relationship("Department", back_populates="students")
    course = db.relationship("Course", back_populates="students")
    academic_records = db.relationship("AcademicRecord", back_populates="student", cascade="all, delete-orphan")


class AcademicRecord(db.Model):
    __tablename__ = "academic_records"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("Student", back_populates="academic_records")
    course = db.relationship("Course", back_populates="academic_records")
