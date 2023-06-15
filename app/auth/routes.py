from flask import render_template, flash, redirect, request, url_for
from app.auth import bp 
from app.extensions import db, limiter
from app.models.account import Account
from app.auth.forms import SignupForm, LoginForm
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user

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
        db.session.add(Account(username = form.username.data, password = generate_password_hash(form.password.data)))
        db.session.commit()
        flash('You have successfully signed up.', 'success')
        return redirect(url_for('auth.signup'))
    return render_template('auth/signup.html', form = form)