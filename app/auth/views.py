"""
learn flask views
"""
# pylint: disable=invalid-name, too-few-public-methods

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm, RegisterForm
from .. import mydb

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """login"""
    loginform_app = LoginForm()
    if loginform_app.validate_on_submit():
        userlogin_check = User.query.filter_by(email=loginform_app.email_input.data).first()
        if userlogin_check is not None and userlogin_check.verify_passwd(loginform_app.passwd_input.data):
            login_user(userlogin_check, loginform_app.remember_me_box.data)
            #return redirect(request.args.get('next') or url_for('main.index'))
            #next参数不知道是哪里来的
            return redirect(url_for('main.index'))
        flash('Invalid email or password.')
    return render_template('auth/login.html', loginform_display=loginform_app)

@auth.route('/logout')
@login_required
def logout():
    """logout"""
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """register new user"""
    registerform_app = RegisterForm()
    if registerform_app.validate_on_submit():
        newuser = User(email=registerform_app.email_reg_input.data,
                       username=registerform_app.username_reg_input.data,
                       passwd=registerform_app.passwd_reg_input.data,
                       role_id=3)
        mydb.session.add(newuser)
        flash('You account is created.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', registerform_display=registerform_app)