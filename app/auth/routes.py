from flask import render_template, flash, redirect, request, url_for, session
from app.auth import bp 
from app.extensions import db, limiter, mail
from app.models.account import Account
from app.auth.forms import SignupForm, LoginForm, NewPasswordForm, ResetPasswordForm
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import os

serializer = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))

@bp.route('/login', methods = ['GET', 'POST'])
@limiter.limit('10/minute')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Account.query.filter_by(username = form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('You have successfully logged in.', 'success')
            return redirect(request.args.get('next') or url_for('main.dashboard'))
        else:
            flash('Username or password is wrong.', 'danger')
    return render_template('auth/login.html', form = form)

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

    