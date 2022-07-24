from flask import Blueprint, render_template, redirect, url_for,flash, request,jsonify, session
from database import db
from models import Scholarship, Student, AppliedScholarship

student = Blueprint('student', __name__, url_prefix='/student')

# student Home/Dashboard
@student.route('/', methods=['GET','POST'])
def home():
    if not auth():
        return redirect(url_for('student.login'))
    scholarships = Scholarship.query.all()
    studid = session['studentID']
    return render_template('student/home.html',scholarships=scholarships,studid=studid)


@student.route('/applied-scholarship', methods=['GET','POST'])
def appliedschol():
    studid = session['studentID']
    applied_scholarships = AppliedScholarship.query.filter_by(student_id=studid).all()
    scholarships = Scholarship.query.all()
    return render_template('student/applied-schol.html',applied_scholarships=applied_scholarships,scholarships=scholarships)


@student.route('/apply/<sid>/<studid>',methods=['GET','POST'])
def applyscholarship(sid,studid):

    # try:
    #     applied_schol = AppliedScholarshipTable(sid=sid,studid=studid)
    #     db.session.add(applied_schol)
    #     db.session.commit()
    #     flash('Scholarship Applied')
    # except:
    #     flash('Already applied for scholarship')

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
