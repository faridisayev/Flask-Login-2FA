from flask import render_template, flash, redirect, request, url_for, session
from app.auth import bp 
from app.extensions import db, limiter, mail
from app.models.account import Account
from app.auth.forms import SignupForm, LoginForm, NewPasswordForm, ResetPasswordForm, TOTPLoginForm
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import os, pyotp, re

serializer = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))

@bp.route('/login', methods = ['GET', 'POST'])
@limiter.limit('10/minute')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if re.match(r'^[a-zA-Z0-9_-]{3,20}$', form.email_or_username.data):
            user = Account.query.filter_by(username = form.email_or_username.data).first()
        else:
            user = Account.query.filter_by(email = form.email_or_username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            if user.enabled_2fa:
                token = serializer.dumps((user.username, form.remember_me.data, request.args.get('next')), salt = 'second_factor_auth')
                return redirect(url_for('auth.second_factor_auth', token = token))
            login_user(user, remember=form.remember_me.data)
            flash('You have successfully logged in.', 'success')
            return redirect(request.args.get('next') or url_for('main.dashboard'))
        else:
            flash('Username or password is wrong.', 'danger')
    return render_template('auth/login.html', form = form)

@bp.route('/second_factor_auth/<token>', methods = ['GET', 'POST'])
@limiter.limit('10/minute')
def second_factor_auth(token):
    try:
        username, remember_me, next = serializer.loads(token, salt = 'second_factor_auth', max_age = 180)
    except SignatureExpired:
        flash('Token signature has expired, please login again.', 'danger')
    except BadSignature:
        flash('Bad signature, please login again..', 'danger')

    form = TOTPLoginForm()
    if form.validate_on_submit():
        user = Account.query.filter_by(username = username).first()
        digits = [str(form.totp_digit_1.data), str(form.totp_digit_2.data), str(form.totp_digit_3.data), str(form.totp_digit_4.data), str(form.totp_digit_5.data), str(form.totp_digit_6.data)]
        totp = int(''.join(digits))
        if pyotp.totp.TOTP(user.secret_key).verify(totp):
            login_user(user, remember = remember_me)
            return redirect(next or url_for('main.dashboard'))
        else:
            flash('Incorrect TOTP code, could not verify user.', 'danger')

    return render_template('auth/second_factor_auth.html', form = form)

@bp.route('/signup', methods = ['GET', 'POST'])
@limiter.limit('10/minute')
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        db.session.add(Account(username = form.username.data, email = form.email.data, password = generate_password_hash(form.password.data)))
        db.session.commit()
        logout_user()
        flash('You have successfully signed up.', 'success')
        return redirect(url_for('auth.signup'))
    return render_template('auth/signup.html', form = form)

@bp.route('/reset_password', methods = ['GET', 'POST'])
@limiter.limit('10/minute')
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        link = url_for('auth.new_password', token = serializer.dumps(form.email.data, salt = 'verify'), _external = True)
        mail.send(Message('Reset Password', sender = os.environ.get('MAIL_USERNAME'), recipients = [form.email.data], body = f'Click this link to reset your password: {link}'))
        flash(f'Verification link has been sent to {form.email.data}', 'success')
        return redirect(url_for('auth.reset_password'))
    return render_template('auth/reset_password.html', form = form)

@bp.route('/new_password/<token>', methods = ['GET', 'POST'])
@limiter.limit('10/minute')
def new_password(token):

    try:
        email = serializer.loads(token, max_age = 180, salt = 'verify')
    except SignatureExpired:
        flash('Signature has been expired, could not verify user.', 'danger')
    except BadSignature:
        flash('Bad signature, could not verify user.', 'danger') 

    form = NewPasswordForm()
    if form.validate_on_submit():
        user = Account.query.filter_by(email = email).first()
        user.password = generate_password_hash(form.new_password.data)
        db.session.add(user)
        db.session.commit()
        flash('Password has been successfully reset.', 'success')
    return render_template('auth/new_password.html', form = form)

    