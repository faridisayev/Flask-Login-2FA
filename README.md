# Complete-Flask-App-With-Blueprint
This is a simple Flask-Login application.
It features 2 Factor Authentication with Google Authenticator, and also Mail verification for password reset. 

There are 2 blueprints in Flask-Login.
1. Auth Blueprint handles authentication process (everything up to the moment the user is logged in).
2. Main Blueprint handles main processes (changing username or email or setting up 2 factor authentication).

Email and username of the user are unique and can be used while logging in to their account. 
Important to note, a user is unable to retrieve their account in case they delete Google Authenticator or remove their account from Google Authenticator.

I have also added recaptcha, rate limiting and CSRF tokens to my forms.
In addition, forms with 2FA have additional token that expires in 2 minutes (120 seconds) and prompts user to log in again.

# Setup
In case you have downloaded the repo, create flask-run.sh to run the application smoothly.
flask-run.sh should set up environmental variables which store sensitive data.

Mine looks like this:

export FLASK_APP=app
export FLASK_ENV=development
export FLASK_DEBUG=true
export PYTHONDONTWRITEBYTECODE=abc
export MAIL_USERNAME=MY_MAIL_USERNAME
export MAIL_PASSWORD=MY_MAIL_PASSWORD
export SECRET_KEY=MY_SECRET_KEY
export RECAPTCHA_SITE_KEY=MY_RECAPTCHA_SITE_KEY
export RECAPTCHA_SECRET_KEY=MY_RECAPTCHA_SECRET_KEY
flask run
