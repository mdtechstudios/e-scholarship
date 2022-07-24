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
    is_approved = db.Column(db.Boolean, default=False)
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
    aadhar = db.Column(db.String(500),nullable=False)
    marks_card = db.Column(db.String(500),nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    def __repr__(self):
        return '<AdditionalInfo %r>' % self.id