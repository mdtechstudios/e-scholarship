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


# student Home/Dashboard
@student.route('/view-scholarships', methods=['GET','POST'])
def viewschol():
    if not auth():
        return redirect(url_for('student.login'))
    scholarships = Scholarship.query.filter_by(is_closed=False).all()
    studid = session['studentID']
    student = Student.query.filter_by(id=studid).first()
    return render_template('student/view-schol.html',scholarships=scholarships,studid=studid,student=student)


@student.route('/applied-scholarship', methods=['GET','POST'])
def appliedschol():
    studid = session['studentID']
    applied_scholarships = AppliedScholarship.query.filter_by(student_id=studid).all()
    scholarships = Scholarship.query.all()
    student = Student.query.filter_by(id=studid).first()
    return render_template('student/applied-schol.html',student=student,applied_scholarships=applied_scholarships,scholarships=scholarships)



@student.route('/apply/<id>/<studid>', methods=['GET','POST'])
def apply(id,studid):
    if request.method == 'POST':
        data = request.form
        print(data)

        # Get All Files
        aadhar_file = request.files['aadhar']
        marks_card_sslc_file = request.files['marks_card_sslc']
        marks_card_puc_file = request.files['marks_card_puc']
        marks_card_degree_file = request.files['marks_card_degree']
        income_cert_file = request.files['income_cert']
        fees_receipt_file = request.files['fees_receipt']

        # Get File Names
        aadhar = aadhar_file.filename
        marks_card_sslc = marks_card_sslc_file.filename
        marks_card_puc = marks_card_puc_file.filename
        marks_card_degree = marks_card_degree_file.filename
        income_cert = income_cert_file.filename
        fees_receipt = fees_receipt_file.filename

        # Get Input Fileds
        aadhar_no = request.form.get('aadhar_no')
        marks_card_sslc_no = request.form.get('marks_card_sslc_no')
        marks_card_puc_no = request.form.get('marks_card_puc_no')
        marks_card_degree_no =  request.form.get('marks_card_degree_no')

        # Save file to OS
        aadhar_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], aadhar))
        marks_card_sslc_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], marks_card_sslc))
        marks_card_puc_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], marks_card_puc))
        marks_card_degree_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], marks_card_degree))
        income_cert_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], income_cert))
        fees_receipt_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], fees_receipt))

        hasData = AppliedScholarship.query.filter_by(scholarship_id=id,student_id=studid).all()
        print(hasData)
        if hasData != []:
            flash('Already applied for scholarship')
            return redirect(url_for('student.viewschol'))
    
        # Insert Applied Scholarship
        applied_schol = AppliedScholarship(scholarship_id=id,student_id=studid)
        db.session.add(applied_schol)
        db.session.commit()

        # Insert Additional Info
        add_info = AdditionalInfo(
            aadhar=aadhar,
            aadhar_no = aadhar_no,
            marks_card_sslc = marks_card_sslc,
            marks_card_sslc_no = marks_card_sslc_no,
            marks_card_puc = marks_card_puc,
            marks_card_puc_no = marks_card_puc_no,
            marks_card_degree = marks_card_degree,
            marks_card_degree_no = marks_card_degree_no,
            income_cert = income_cert,
            fees_receipt = fees_receipt,
            student_id = studid,
            scholarship_id = id
        )
        db.session.add(add_info)
        db.session.commit()
        flash('Scholarship Applied')
        return redirect(url_for('student.appliedschol'))
    studid = session['studentID']
    s = Scholarship.query.filter_by(id=id).first()
    student = Student.query.filter_by(id=studid).first()
    return render_template('student/apply-schol.html',id=id,studid=studid,student=student)


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
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        address = request.form.get('address')
        password = request.form.get('password')
        student = Student(name=name,email=email,phoneno=phoneno,dob=dob,gender=gender,address=address,password=password,is_approved=False)
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
