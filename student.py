from flask import Blueprint, render_template, redirect, url_for,flash, request,jsonify, session, current_app
from database import db
from models import Scholarship, Student, AppliedScholarship, AdditionalInfo
import os

student = Blueprint('student', __name__, url_prefix='/student')


# student Home/Dashboard
@student.route('/', methods=['GET','POST'])
def home():
    if not auth():
        return redirect(url_for('student.login'))
    scholarships = Scholarship.query.all()
    studid = session['studentID']
    student = Student.query.filter_by(id=studid).first()
    return render_template('student/home.html',scholarships=scholarships,studid=studid,student=student)


@student.route('/applied-scholarship', methods=['GET','POST'])
def appliedschol():
    studid = session['studentID']
    applied_scholarships = AppliedScholarship.query.filter_by(student_id=studid).all()
    scholarships = Scholarship.query.all()
    student = Student.query.filter_by(id=studid).first()
    return render_template('student/applied-schol.html',student=student,applied_scholarships=applied_scholarships,scholarships=scholarships)



@student.route('/apply/<sid>/<studid>',methods=['GET','POST'])
def applyscholarship(sid,studid):
    hasData = AppliedScholarship.query.filter_by(scholarship_id=sid,student_id=studid).all()
    print(hasData)
    if hasData != []:
        flash('Already applied for scholarship')
    else:
        applied_schol = AppliedScholarship(scholarship_id=sid,student_id=studid)
        db.session.add(applied_schol)
        db.session.commit()
        flash('Scholarship Applied')
    return redirect(url_for('student.home'))


@student.route('/upload', methods = ['POST'])  
def upload():  
    if request.method == 'POST':
        file = request.files['aadhar']
        filee = request.files['markscard']
        student_id = request.form.get('student_id')
        scholarship_id = request.form.get('sid')
        aadhar = file.filename
        marks_card = filee.filename
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], aadhar))
        filee.save(os.path.join(current_app.config['UPLOAD_FOLDER'], marks_card))
        print(aadhar)
        print(marks_card)
        hasData = AppliedScholarship.query.filter_by(scholarship_id=scholarship_id,student_id=student_id).all()
        print(hasData)
        if hasData != []:
            flash('Already applied for scholarship')
            return redirect(url_for('student.home'))
    
        applied_schol = AppliedScholarship(scholarship_id=scholarship_id,student_id=student_id)
        db.session.add(applied_schol)
        db.session.commit()

        add_info = AdditionalInfo(aadhar=str(aadhar),marks_card=str(marks_card),student_id=student_id)
        db.session.add(add_info)
        db.session.commit()
        return redirect(url_for('student.home'))



# Student Regiser
@student.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        phoneno = request.form.get('phoneno')
        password = request.form.get('password')
        student = Student(name=name,email=email,phoneno=phoneno,password=password,is_approved=False)
        db.session.add(student)
        db.session.commit()
        flash('Student successfully registered')
        return redirect(url_for('student.login'))
    return render_template('student/register.html')


# student Login
@student.route('/login', methods=['GET', 'POST'])
def login():
    if auth():
        return redirect(url_for('student.home'))
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        student = Student.query.filter_by(email=email, password=password).first()
        print(student)
        db.session.commit()
        if student is None:
            flash('Invalid Email/Password')
            return render_template('student/login.html')
        else:
            session['studentID'] = student.id
            flash('Login Successful')
            return redirect(url_for('student.home'))
    return render_template('student/login.html')


# student Logout
@student.route('/logout', methods=['GET', 'POST'])
def logout():
    if not auth():
        return redirect(url_for('student.login'))
    session['studentID'] = None
    flash('Logout Successful')
    return redirect(url_for('student.login'))



# Check student isLoggedIn
def auth():
    if 'studentID' not in session:
        session['studentID'] = None
    if session['studentID'] is None:
        return False
    else:
        return True
