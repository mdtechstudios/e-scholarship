from flask import Blueprint, render_template, redirect, url_for,flash, request,jsonify, session

student = Blueprint('student', __name__, url_prefix='/student')

# Student Home Page
@student.route('/', methods=['GET','POST'])
def home():
    return 'Student Home Page'