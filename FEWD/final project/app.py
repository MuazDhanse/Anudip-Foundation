from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Set the database path
app.config['DATABASE'] = os.path.join(app.instance_path, 'users.db')

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# Inject dynamic year for footer
@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}

# Home Page Route
@app.route('/')
def home():
    user_email = session.get('user_email', None)
    return render_template('index.html', user_email=user_email)

# About Page Route
@app.route('/about')
def about():
    return render_template('about.html')

# Community Page Route
@app.route('/community')
def community():
    return render_template('community.html')

# Contact Page Route
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Login Page Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_email'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Signup Page Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
            conn.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already registered.', 'danger')
            return redirect(url_for('signup'))
        finally:
            conn.close()

    return render_template('signup.html')

# Logout Route
@app.route('/logout')
def logout():
    session.clear()  # Clear the user session
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
