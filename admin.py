from flask import Blueprint, render_template, redirect, url_for,flash, request,jsonify, session
from database import db
from models import AdminTable, Scholarship, AppliedScholarship, Student, AdditionalInfo

admin = Blueprint('admin', __name__, url_prefix='/admin')


# Admin Home/Dashboard
@admin.route('/', methods=['GET','POST'])
def home():
    if not auth():
        return redirect(url_for('admin.login'))
    return render_template('admin/home.html')


# View All Students
@admin.route('/students', methods=['GET','POST'])
def viewstudents():
    if not auth():
        return redirect(url_for('admin.login'))
    students = Student.query.all()
    # studid = session['studentID']
    return render_template('admin/view-students.html', students=students)



# View All Students
@admin.route('/delete-student/<id>', methods=['GET','POST'])
def deletestudent(id):
    if not auth():
        return redirect(url_for('admin.login'))
    schol = AppliedScholarship.query.filter_by(student_id=id).delete()
    s = Student.query.filter_by(id=id).delete()
    db.session.commit()
    flash("Student Deleted")
    # studid = session['studentID']
    return redirect(url_for("admin.viewstudents"))

# Approve Student
@admin.route('/approve-student/<id>',methods=['GET','POST'])
def studapprove(id):
    if not auth():
        return redirect(url_for('admin.login'))
    s = Student.query.filter_by(id=id).first()
    s.is_approved = True
    db.session.commit()
    flash("Student Approved")
    return redirect(url_for('admin.viewstudents'))



# Approve Student
@admin.route('/reject-student/<id>',methods=['GET','POST'])
def studreject(id):
    if not auth():
        return redirect(url_for('admin.login'))
    s = Student.query.filter_by(id=id).first()
    s.is_approved = False
    db.session.commit()
    flash("Student Not Approved")
    return redirect(url_for('admin.viewstudents'))


# Add Scholarship
@admin.route('/add-scholarship', methods=['GET','POST'])
def addscholarship():
    if not auth():
        return redirect(url_for('admin.login'))
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        schol = Scholarship(name=name,description=description, is_closed=False)
        db.session.add(schol)
        db.session.commit()
        flash('Scholarship added')
        return redirect(url_for('admin.viewscholarships'))
    return render_template('admin/add-scholarship.html')


# View All Scholarships
@admin.route('/scholarships', methods=['GET','POST'])
def viewscholarships():
    if not auth():
        return redirect(url_for('admin.login'))
    scholarships = Scholarship.query.all()
    # studid = session['studentID']
    return render_template('admin/view-scholarships.html', scholarships=scholarships)


# View Individual Scholarship Application by ID
@admin.route('/scholarship/<id>', methods=['GET','POST'])
def viewscholarship(id):
    if not auth():
        return redirect(url_for('admin.login'))
    scholarships = Scholarship.query.all()
    applied_students = AppliedScholarship.query.filter_by(scholarship_id=id).all()
    add_info = AdditionalInfo.query.all()
    # studid = session['studentID']
    return render_template('admin/view-applications.html', applied_students=applied_students,add_info=add_info)


@admin.route('/view-student/<scholarship_id>/<studid>', methods=['GET','POST'])
def viewstud(scholarship_id,studid):
    if not auth():
        return redirect(url_for('admin.login'))
    stud_info = Student.query.filter_by(id=studid).first()
    add_info = AdditionalInfo.query.filter_by(scholarship_id=scholarship_id,student_id=studid).first()
    return render_template('admin/view-student.html',add_info=add_info,stud_info=stud_info)
    

# Generagte Applied Stduent report
@admin.route('/generate-report/<id>', methods=['GET','POST'])
def generatereport(id):
    if not auth():
        return redirect(url_for('admin.login'))
    scholarships = Scholarship.query.all()
    applied_students = AppliedScholarship.query.filter_by(scholarship_id=id,is_approved=True).all()
    # studid = session['studentID']
    return render_template('admin/application-report.html', applied_students=applied_students)


# Update Scholarship
@admin.route('/update-scholarship/<id>', methods=['GET','POST'])
def updatescholarship(id):
    if not auth():
        return redirect(url_for('admin.login'))
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get('description')
        s = Scholarship.query.filter_by(id=id).first()
        s.name = name
        s.description = description
        db.session.commit()
        flash('Scholarship Updated')
        return redirect(url_for('admin.viewscholarships'))
    s = Scholarship.query.filter_by(id=id).first()
    db.session.commit()
    # flash("Scholarship Updated")
    # return redirect(url_for('admin.viewscholarships'))
    return render_template('admin/update-scholarship.html',id=id,s=s)



# Delete Scholarship
@admin.route('/delete-scholarship/<id>', methods=['GET','POST'])
def deletescholarship(id):
    if not auth():
        return redirect(url_for('admin.login'))
    s = Scholarship.query.filter_by(id=id).first()
    if s.is_closed == True:
        s.is_closed = False
    else:
        s.is_closed = True
    db.session.commit()
    flash("Scholarship Disabled")
    return redirect(url_for('admin.viewscholarships'))


# Scholarship Approve
@admin.route('/sapprove/<id>/<studid>')
def sapprove(id,studid):
    if not auth():
        return redirect(url_for('admin.login'))
    s = AppliedScholarship.query.filter_by(scholarship_id=id,student_id=studid).first()
    s.is_approved = True
    db.session.commit()
    flash("Student Approved")
    return redirect(url_for('admin.viewscholarship',id=id))


# Scholarship reject
@admin.route('/sreject/<id>/<studid>')
def sreject(id,studid):
    if not auth():
        return redirect(url_for('admin.login'))
    s = AppliedScholarship.query.filter_by(scholarship_id=id,student_id=studid).first()
    s.is_approved = False
    db.session.commit()
    flash("Student Rejected")
    return redirect(url_for('admin.viewscholarship',id=id))


# Admin Login
@admin.route('/login', methods=['GET', 'POST'])
def login():
    if auth():
        return redirect(url_for('admin.home'))
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        admin = AdminTable.query.filter_by(email=email, password=password).first()
        db.session.commit()
        if admin is None:
            flash('Invalid Email/Password')
            return render_template('admin/login.html')
        else:
            session['adminID'] = admin.id
            return redirect(url_for('admin.home'))
    return render_template('admin/login.html')



# Admin Logout
@admin.route('/logout', methods=['GET', 'POST'])
def logout():
    if not auth():
        return redirect(url_for('admin.login'))
    session['adminID'] = None
    return redirect(url_for('admin.login'))


# Check isLoggedIn
def auth():
    if 'adminID' not in session:
        session['adminID'] = None
    if session['adminID'] is None:
        return False
    else:
        return True
