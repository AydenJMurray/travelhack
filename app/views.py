from flask import render_template, flash, redirect, request, url_for, session, g
from app import app, db, login_manager
from .forms import LoginForm, RegisterForm, NewPostForm
from flask.ext.login import current_user, login_required, login_user, logout_user
from .models import User, Post
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = NewPostForm()
    if form.validate_on_submit:
        print form
    return render_template('index.html',
                            title='Home',
                            data)
