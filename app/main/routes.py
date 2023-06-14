from flask import render_template, flash, redirect, url_for
from app.main import bp 
from flask_login import login_required, logout_user, current_user
from app.extensions import db
from app.models.account import Account

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/account')
@login_required
def account():
    return render_template('account.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/delete_account/<int:id>')
@login_required
def delete_account(id):
    db.session.delete(Account.query.filter_by(id = id).first())
    db.session.commit()
    flash('Your account was successfully deleted.', 'success')
    return redirect(url_for('auth.login'))