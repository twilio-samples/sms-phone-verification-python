import os
import sqlite3
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, request, redirect, url_for, render_template, session, g, flash
import bcrypt
from twilio.rest import Client

load_dotenv()

required_vars = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'VERIFY_SERVICE_SID']
missing = [v for v in required_vars if not os.environ.get(v)]
if missing:
    print('\n❌ Missing required environment variables:')
    for v in missing:
        print(f'   - {v}')
    print('\nCopy .env.example to .env and fill in your Twilio credentials.\n')
    exit(1)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

DATABASE = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

twilio_client = Client(
    os.environ['TWILIO_ACCOUNT_SID'],
    os.environ['TWILIO_AUTH_TOKEN']
)
VERIFY_SERVICE_SID = os.environ['VERIFY_SERVICE_SID']


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            verified INTEGER DEFAULT 0
        )
    ''')
    db.commit()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def get_current_user():
    if 'user_id' not in session:
        return None
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    return dict(user) if user else None


@app.route('/')
def index():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    if not user['verified']:
        return redirect(url_for('verify'))
    return render_template('dashboard.html', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if get_current_user():
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone_number = request.form.get('phone_number')

        error = None

        if not username or not password or not phone_number:
            error = 'All fields are required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        else:
            db = get_db()
            existing = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
            if existing:
                error = 'Username already exists.'

        if error:
            flash(error, 'error')
            return render_template('register.html')

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        db = get_db()
        cursor = db.execute(
            'INSERT INTO users (username, password, phone_number) VALUES (?, ?, ?)',
            (username, hashed.decode('utf-8'), phone_number)
        )
        db.commit()

        session['user_id'] = cursor.lastrowid
        return redirect(url_for('verify'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if get_current_user():
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            flash('Invalid username or password.', 'error')
            return render_template('login.html')

        session['user_id'] = user['id']

        if user['verified']:
            return redirect(url_for('index'))
        return redirect(url_for('verify'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/verify', methods=['GET', 'POST'])
@login_required
def verify():
    user = get_current_user()

    if user['verified']:
        return redirect(url_for('index'))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'send':
            try:
                twilio_client.verify.v2.services(VERIFY_SERVICE_SID) \
                    .verifications \
                    .create(to=user['phone_number'], channel='sms')
                flash('Verification code sent to your phone.', 'success')
            except Exception as e:
                flash(f'Error sending code: {str(e)}', 'error')

        elif action == 'check':
            code = request.form.get('code')
            if not code:
                flash('Please enter the verification code.', 'error')
            else:
                try:
                    verification_check = twilio_client.verify.v2.services(VERIFY_SERVICE_SID) \
                        .verification_checks \
                        .create(to=user['phone_number'], code=code)

                    if verification_check.status == 'approved':
                        db = get_db()
                        db.execute('UPDATE users SET verified = 1 WHERE id = ?', (user['id'],))
                        db.commit()
                        flash('Phone number verified successfully!', 'success')
                        return redirect(url_for('index'))
                    else:
                        flash(f'Verification failed: {verification_check.status}', 'error')
                except Exception as e:
                    flash(f'Error verifying code: {str(e)}', 'error')

    return render_template('verify.html', user=user)


if __name__ == '__main__':
    with app.app_context():
        init_db()
    port = int(os.environ.get('PORT', 5000))
    print(f'Server running on http://localhost:{port}')
    app.run(host='0.0.0.0', port=port, debug=True)
