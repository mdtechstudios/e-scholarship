from database import db


# Admin Table
class AdminTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return '<Admin %r>' % self.email


# Student Table
class StudentTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(150),nullable=False)
    phoneno = db.Column(db.Integer,nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return '<Student %r>' % self.email


# Scholarship Table
class ScholarshipTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    def __repr__(self):
        return '<Scholarship %r>' % self.name

