from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional


class StudentForm(FlaskForm):
    student_id = StringField(
        "Student ID",
        validators=[DataRequired(), Length(min=2, max=50)],
    )
    full_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=2, max=150)],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=150)],
    )
    phone = StringField(
        "Phone Number",
        validators=[DataRequired(), Length(min=7, max=30)],
    )
    department_id = SelectField("Department", coerce=int, validators=[DataRequired()])
    course_id = SelectField("Course", coerce=int, validators=[DataRequired()])
    enrollment_date = DateField("Enrollment Date", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Save Student")


class AcademicRecordForm(FlaskForm):
    course_id = SelectField("Course", coerce=int, validators=[DataRequired()])
    academic_year = StringField(
        "Academic Year",
        validators=[DataRequired(), Length(min=4, max=20)],
    )
    semester = StringField(
        "Semester",
        validators=[DataRequired(), Length(min=2, max=20)],
    )
    grade = FloatField(
        "Grade",
        validators=[DataRequired(), NumberRange(min=0, max=100)],
    )
    submit = SubmitField("Add Record")
