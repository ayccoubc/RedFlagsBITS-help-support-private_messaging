# User Profile 


from flask import Flask, render_template, request, redirect,session
import sqlite3
from datetime import datetime
from flask import flash 
import os
app = Flask(__name__)

def generate_secret_key():
    return os.urandom(24).hex()

app.secret_key = generate_secret_key()

# USER PROFILE CODE 

DATABASE = 'user_profiles.db'


def create_tables():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,
                 full_name TEXT NOT NULL,
                 age INTEGER NOT NULL,
                 dob DATE NOT NULL,
                 contact TEXT NOT NULL,
                 emergency_contact TEXT NOT NULL,
                 profile_photo TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS medical_records(id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER NOT NULL,
                 medical_problem TEXT NOT NULL,
                 FOREIGN KEY (user_id) REFERENCES users (id))''')

    conn.commit()
    conn.close()

    create_tables()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        full_name = request.form['full_name']
        age = int(request.form['age'])
        dob = request.form['dob']
        contact = request.form['contact']
        emergency_contact = request.form['emergency_contact']
        profile_photo = request.files['profile_photo']

        if profile_photo:
            profile_photo.save('static/profile_photos/' + profile_photo.filename)

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        c.execute('''INSERT INTO users (full_name, age, dob, contact, emergency_contact, profile_photo)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (full_name, age, dob, contact, emergency_contact, profile_photo.filename))
        conn.commit()
        session['user_id'] = c.lastrowid  # Store the user ID in session
        conn.close()

        flash('Profile created successfully!', 'success')
        return redirect('/')

    return render_template('create_profile.html')



@app.route('/view_profile')
def view_profile():
    user_id = session.get('user_id')  # Get the latest user ID from session

    if user_id:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = c.fetchone()
        conn.close()

        if user:
            return render_template('view_profile.html', user=user)
    
    return render_template('view_profile.html', message='Profile has not been created yet.')


@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    user_id = session.get('user_id')  # Get the latest user ID from session

    if user_id:
        if request.method == 'POST':
            full_name = request.form['full_name']
            age = int(request.form['age'])
            dob = request.form['dob']
            contact = request.form['contact']
            emergency_contact = request.form['emergency_contact']
            profile_photo = request.files['photo']

            if profile_photo:
                profile_photo.save('static/profile_photos/' + profile_photo.filename)

            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()

            c.execute('''UPDATE users SET full_name=?, age=?, dob=?, contact=?, emergency_contact=?, profile_photo=?
                         WHERE id=?''',
                      (full_name, age, dob, contact, emergency_contact, profile_photo.filename, user_id))

            conn.commit()
            conn.close()

            flash('Profile updated successfully!', 'success')
            return redirect('/')

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = c.fetchone()
        conn.close()

        if user:
            return render_template('update_profile.html', user=user)

    return render_template('update_profile.html', message='Profile has not been created yet.')

@app.route('/medical_records', methods=['GET', 'POST'])
def medical_records():
    if request.method == 'POST':
        medical_problem = request.form['medical_problem']

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        user_id = session.get('user_id')  # Get the user ID from session

        c.execute('''INSERT INTO medical_records (user_id, medical_problem)
                     VALUES (?, ?)''',
                  (user_id, medical_problem))

        conn.commit()
        conn.close()

        return redirect('/')

    user_id = session.get('user_id')  # Get the user ID from session

    if user_id:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = c.fetchone()

        conn.close()

        if user:
            return render_template('medical_records.html', user=user)

    return render_template('medical_records.html', user=None, message='Profile has not been created yet.')



if __name__ == '__main__':
    create_tables()
    app.run(debug=True)