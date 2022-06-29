from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from admin import admin
from models import db
from student import student
import os
from os.path import join, dirname, realpath

app = Flask(__name__)

app.secret_key = '5accdb11b2c10a78d7c92c5fa102ea77fcd50c2058b00f6e'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/escholarship"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "escholarship"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
UPLOADS_PATH = join(dirname(realpath(__file__)), 'static\\uploads')
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

app.register_blueprint(admin)
app.register_blueprint(student)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('home.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(debug=True)
