from flask import Blueprint, render_template, redirect, url_for,flash, request,jsonify, session
from database import db
from models import AdminTable, StudentTable, ScholarshipTable

admin = Blueprint('admin', __name__, url_prefix='/admin')


# Admin Home/Dashboard
@admin.route('/', methods=['GET','POST'])
def home():
    if not auth():
        return redirect(url_for('admin.login'))
    return render_template('admin/home.html')


# View All Scholarships
@admin.route('/scholarships', methods=['GET','POST'])
def viewscholarships():
    if not auth():
        return redirect(url_for('admin.login'))
    scholarships = ScholarshipTable.query.all()
    return render_template('admin/view-scholarships.html',scholarships=scholarships)



# View Scholarship by ID
@admin.route('/scholarship/<int:sid>', methods=['GET','POST'])
def viewscholarship(sid):
    if not auth():
        return redirect(url_for('admin.login'))
    scholarship = ScholarshipTable.query.filter_by(id=sid).first()
    return render_template('admin/view-scholarship.html',scholarship=scholarship)


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
