"""
learn flask views
"""
# pylint: disable=invalid-name

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegisterForm
from .. import mydb
from ..email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """login"""
    loginform_app = LoginForm()
    if loginform_app.validate_on_submit():
        userlogin_check = User.query.filter_by(email=loginform_app.email_input.data).first()
        if userlogin_check is not None and userlogin_check.verify_passwd(loginform_app.passwd_input.data): # pylint: disable=line-too-long
            login_user(userlogin_check, loginform_app.remember_me_box.data)
            #return redirect(request.args.get('next') or url_for('main.index'))
            #next参数不知道是哪里来的
            return redirect(url_for('main.index'))
        flash('Invalid email or password.')
    return render_template('auth/login.html', loginform_display=loginform_app)

@auth.route('/logout')
@login_required #login_manager unauthorized 强制跳转到login_view
def logout():
    """logout"""
    logout_user()
    flash('You have been logged out.') #这个flash到main.index上去了
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
        mydb.session.add(newuser)# pylint: disable=no-member
        mydb.session.commit()# pylint: disable=no-member 需要立刻提交数据库以获得id
        token = newuser.generate_confirmation_token()
        send_email(newuser.email, 'Confirm Your Account',
                   'auth/email/confirm', mailuser=newuser, token=token)
        flash('A confirmation email sent.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', registerform_display=registerform_app)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """确认邮件url路由"""
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request(): 
    """限制未认证用户的活动范围"""
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    """超出范围就转到提示页"""
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    """重新发送确认邮件"""
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', mailuser=current_user, token=token)
    flash('A confirmation email sent.')
    return redirect(url_for('main.index'))