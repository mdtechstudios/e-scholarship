from database import db


# Admin Table
class AdminTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=True)
    email = db.Column(db.String(200),unique=True,nullable=False)
    password = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return '<Admin %r>' % self.email


# Student Table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(500),nullable=False, unique=True)
    phoneno = db.Column(db.Integer,nullable=False,unique=True)
    password = db.Column(db.String(50),nullable=False)
    dob = db.Column(db.String(50),nullable=False)
    gender = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(500),nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    # scholarships = db.relationship('Scholarship', backref='schol')
    applied_scholarship = db.relationship('AppliedScholarship',backref='appliedschol')
    additional_info = db.relationship('AdditionalInfo', backref='addinfo')
    def __repr__(self):
        return '<Student %r>' % self.name


# Scholarship Table
class Scholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500),nullable=False)
    description = db.Column(db.String(500),nullable=False)
    is_closed = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return '<Scholarship %r>' % self.id

# AppliedScholarship Table
class AppliedScholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scholarship_id = db.Column(db.Integer, db.ForeignKey('scholarship.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    is_approved = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return '<AppliedScholarship %r>' % self.id


# AdditionalInfo Table
class AdditionalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aadhar = db.Column(db.String(500),nullable=True)
    aadhar_no = db.Column(db.String(500),nullable=True)
    marks_card_sslc = db.Column(db.String(500),nullable=True)
    marks_card_sslc_no = db.Column(db.String(500),nullable=True)
    marks_card_puc = db.Column(db.String(500),nullable=True)
    marks_card_puc_no = db.Column(db.String(500),nullable=True)
    marks_card_degree = db.Column(db.String(500),nullable=True)
    marks_card_degree_no = db.Column(db.String(500),nullable=True)
    income_cert = db.Column(db.String(500),nullable=True)
    fees_receipt = db.Column(db.String(500),nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    scholarship_id = db.Column(db.Integer, db.ForeignKey('scholarship.id'))
    def __repr__(self):
        return '<AdditionalInfo %r>' % self.id