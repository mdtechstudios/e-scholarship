from flask import Blueprint, render_template, redirect, url_for,flash, request,jsonify, session

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Admin Dashboard
@admin.route('/', methods=['GET','POST'])
def home():
    return 'Admin Dashboard'