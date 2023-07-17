from flask import Flask, render_template, request, url_for, redirect,session
import sqlite3

app = Flask(__name__)

DATABASE2 = 'help_msgphysician.db'

def create_tables2():
    conn = sqlite3.connect(DATABASE2)
    c = conn.cursor()
    
    
    c.execute('''CREATE TABLE IF NOT EXISTS msg_physician(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                doctor_name TEXT NOT NULL,
                message TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS help_text(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT ,
                text TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )''')
    
    conn.commit()
    conn.close()

create_tables2()

@app.route('/msg_physician', methods=['GET', 'POST'])
def msg_physician():
    user_id = session.get('user_id')  # Get the latest user ID from session

    if not user_id:
        return render_template('create_profile.html', message='Create your profile first.')

    if request.method == 'POST':
        doctor_name = request.form['doctor']
        message = request.form['message']

        conn = sqlite3.connect(DATABASE2)
        c = conn.cursor()

        c.execute('''INSERT INTO msg_physician(user_id, doctor_name, message)
                     VALUES (?, ?, ?)''', (user_id, doctor_name, message))

        conn.commit()
        conn.close()

        return redirect('/')

    # Retrieve the list of doctors from the database or use a predefined list
    doctors = [
    'Dr. Smith',
    'Dr. Johnson',
    'Dr. Williams',
    'Dr. Jones',
    'Dr. Brown',
    'Dr. Davis',
    'Dr. Miller',
    'Dr. Wilson',
    'Dr. Anderson',
    'Dr. Taylor'
]
  

    return render_template('msg_physician.html', doctors=doctors)