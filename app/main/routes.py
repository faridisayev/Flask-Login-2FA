from flask import render_template, flash, redirect, url_for, request
from app.main import bp 
from flask_login import login_required, logout_user, current_user, fresh_login_required
from app.extensions import db
from app.models.account import Account
from app.main.forms import UpdateAccountForm
from app.auth.forms import TOTPLoginForm as SetupTwoFactorAuthenticationForm
from urllib import parse
import pyotp

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

@bp.route('/update_account', methods = ['GET', 'POST'])
@fresh_login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.username.data: current_user.username = form.username.data
        if form.email.data: current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
    return render_template('update_account.html', form = form)

@bp.route('/setup_2fa', methods = ['GET', 'POST'])
@fresh_login_required
def setup_2fa():

    if current_user.enabled_2fa:
        return redirect(url_for('main.account'))

    form = SetupTwoFactorAuthenticationForm()

    if form.validate_on_submit():

        digits = [str(form.totp_digit_1.data), str(form.totp_digit_2.data), str(form.totp_digit_3.data), str(form.totp_digit_4.data), str(form.totp_digit_5.data), str(form.totp_digit_6.data)]
        totp = int(''.join(digits))

        if not pyotp.TOTP(current_user.secret_key).verify(totp):
            flash('The code you provided is wrong. Please scan new qrcode and try again.', 'danger')
            return redirect(url_for('main.setup_2fa'))
        
        current_user.enabled_2fa = True
        db.session.commit()
        return redirect(url_for('main.account'))

    current_user.secret_key = pyotp.random_base32()
    db.session.commit()
    uri = pyotp.totp.TOTP(current_user.secret_key).provisioning_uri(name = current_user.username, issuer_name = 'Flask App')
    qrcode_url = "https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl=" + parse.quote(uri, safe='')

    return render_template('setup_2fa.html', form = form, qrcode_url = qrcode_url)

@bp.route('/disable_2fa')
@fresh_login_required
def disable_2fa():
    current_user.enabled_2fa = False
    db.session.commit()
    return redirect(url_for('main.account'))