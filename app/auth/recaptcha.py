from flask import abort
import requests, os

def verify_response(request):
    verify_response = requests.post(url = f"https://www.google.com/recaptcha/api/siteverify?secret={os.environ.get('RECAPTCHA_SECRET_KEY')}&response={request.form['g-recaptcha-response']}").json()
    if not verify_response['success'] or verify_response['score'] < 0.5:
        abort(401)