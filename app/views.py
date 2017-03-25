from flask import render_template, flash, redirect, request, url_for, session, g
from app import app
from .forms import LoginForm, RegisterForm, NewPostForm
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = NewPostForm()
    if form.validate_on_submit:
        print form

    data = {"a": "b"}
    return render_template('index.html',
                            title='Home',
                            data=data)
