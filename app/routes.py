from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import or_

from .forms import AcademicRecordForm, StudentForm
from .models import AcademicRecord, Course, Department, Student, db

main = Blueprint("main", __name__)


@main.route("/")
def dashboard():
    total_students = Student.query.count()
    recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()
    return render_template("dashboard.html", total_students=total_students, recent_students=recent_students)


@main.route("/students", methods=["GET"])
def students():
    query = request.args.get("q", "").strip()
    department_id = request.args.get("department", "", type=int)
    course_id = request.args.get("course", "", type=int)

    student_query = Student.query

    if query:
        student_query = student_query.filter(
            or_(
                Student.student_id.ilike(f"%{query}%"),
                Student.full_name.ilike(f"%{query}%"),
                Student.email.ilike(f"%{query}%"),
            )
        )

    if department_id:
        student_query = student_query.filter(Student.department_id == department_id)

    if course_id:
        student_query = student_query.filter(Student.course_id == course_id)

    students_list = student_query.order_by(Student.created_at.desc()).all()
    departments = Department.query.order_by(Department.name).all()
    courses = Course.query.order_by(Course.name).all()

    return render_template(
        "students.html",
        students=students_list,
        departments=departments,
        courses=courses,
        selected_department=department_id,
        selected_course=course_id,
        search_query=query,
    )


@main.route("/students/new", methods=["GET", "POST"])
def add_student():
    form = StudentForm()
    form.department_id.choices = [(dept.id, dept.name) for dept in Department.query.order_by(Department.name).all()]
    form.course_id.choices = [(course.id, course.name) for course in Course.query.order_by(Course.name).all()]

    if request.method == "POST":
        if form.validate_on_submit():
            student_id = form.student_id.data.strip()
            email = form.email.data.strip().lower()
            department_id = form.department_id.data
            course_id = form.course_id.data

            if Student.query.filter_by(student_id=student_id).first():
                form.student_id.errors.append("Student ID already exists.")
                flash("Student ID already exists.", "error")
            elif Student.query.filter_by(email=email).first():
                form.email.errors.append("Email address already exists.")
                flash("Email address already exists.", "error")
            else:
                course = Course.query.get(course_id)
                if course is None or course.department_id != department_id:
                    form.course_id.errors.append("Selected course does not belong to the chosen department.")
                    flash("Selected course does not belong to the chosen department.", "error")
                else:
                    student = Student(
                        student_id=student_id,
                        full_name=form.full_name.data.strip(),
                        email=email,
                        phone=form.phone.data.strip(),
                        department_id=department_id,
                        course_id=course_id,
                        enrollment_date=form.enrollment_date.data,
                    )
                    db.session.add(student)
                    try:
                        db.session.commit()
                        flash("Student added successfully.", "success")
                        return redirect(url_for("main.students"))
                    except Exception:
                        db.session.rollback()
                        flash("Unable to save student. Please check your data and try again.", "error")

    return render_template("student_form.html", form=form, action="Add", page_title="Add Student")


@main.route("/students/<int:id>/edit", methods=["GET", "POST"])
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    form.department_id.choices = [(dept.id, dept.name) for dept in Department.query.order_by(Department.name).all()]
    form.course_id.choices = [(course.id, course.name) for course in Course.query.order_by(Course.name).all()]

    if request.method == "POST":
        if form.validate_on_submit():
            student_id = form.student_id.data.strip()
            email = form.email.data.strip().lower()
            duplicate_student = Student.query.filter(Student.student_id == student_id, Student.id != student.id).first()
            duplicate_email = Student.query.filter(Student.email == email, Student.id != student.id).first()

            if duplicate_student:
                form.student_id.errors.append("Student ID already exists.")
                flash("Student ID already exists.", "error")
            elif duplicate_email:
                form.email.errors.append("Email address already exists.")
                flash("Email address already exists.", "error")
            else:
                course = Course.query.get(form.course_id.data)
                if course is None or course.department_id != form.department_id.data:
                    form.course_id.errors.append("Selected course does not belong to the chosen department.")
                    flash("Selected course does not belong to the chosen department.", "error")
                else:
                    student.student_id = student_id
                    student.full_name = form.full_name.data.strip()
                    student.email = email
                    student.phone = form.phone.data.strip()
                    student.department_id = form.department_id.data
                    student.course_id = form.course_id.data
                    student.enrollment_date = form.enrollment_date.data
                    student.updated_at = datetime.utcnow()
                    try:
                        db.session.commit()
                        flash("Student information updated successfully.", "success")
                        return redirect(url_for("main.student_detail", id=student.id))
                    except Exception:
                        db.session.rollback()
                        flash("Unable to update student information. Please try again.", "error")

    if request.method == "GET":
        form.student_id.data = student.student_id
        form.full_name.data = student.full_name
        form.email.data = student.email
        form.phone.data = student.phone
        form.department_id.data = student.department_id
        form.course_id.data = student.course_id
        form.enrollment_date.data = student.enrollment_date

    return render_template("student_form.html", form=form, action="Edit", page_title="Edit Student")


@main.route("/students/<int:id>", methods=["GET", "POST"])
def student_detail(id):
    student = Student.query.get_or_404(id)
    form = AcademicRecordForm()
    form.course_id.choices = [(course.id, course.name) for course in Course.query.order_by(Course.name).all()]

    if request.method == "POST":
        if form.validate_on_submit():
            course = Course.query.get(form.course_id.data)
            if course is None:
                form.course_id.errors.append("Please select a valid course.")
                flash("Please select a valid course.", "error")
            else:
                record = AcademicRecord(
                    student_id=student.id,
                    course_id=course.id,
                    academic_year=form.academic_year.data.strip(),
                    semester=form.semester.data.strip(),
                    grade=form.grade.data,
                )
                db.session.add(record)
                try:
                    db.session.commit()
                    flash("Academic record added successfully.", "success")
                    return redirect(url_for("main.student_detail", id=student.id))
                except Exception:
                    db.session.rollback()
                    flash("Unable to save academic record. Please check the values and try again.", "error")

    return render_template("student_detail.html", student=student, form=form, records=student.academic_records)


@main.route("/students/<int:id>/delete", methods=["POST"])
def delete_student(id):
    student = Student.query.get_or_404(id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash("Student deleted successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Unable to delete the student record.", "error")
    return redirect(url_for("main.students"))


@main.app_errorhandler(404)
def page_not_found(error):
    return render_template("404.html", error=error), 404


@main.app_errorhandler(500)
def internal_server_error(error):
    return render_template("500.html", error=error), 500
