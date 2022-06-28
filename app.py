from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from admin import admin
from student import student
import os
from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static\\uploads')

app = Flask(__name__)
app.secret_key = '5accdb11b2c10a78d7c92c5fa102ea77fcd50c2058b00f6e'
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
app.register_blueprint(admin)
app.register_blueprint(student)


@app.route('/')
def home():
    return 'Home Page'


@app.errorhandler(404)
def not_found(e):
    return 'Page not found'


if __name__ == '__main__':
    app.run(debug=True)
