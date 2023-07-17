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

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/help', methods=['GET', 'POST'])
def help():
    user_id = session.get('user_id')  # Get the latest user ID from session

    if not user_id:
        return render_template('help.html', message='Create your profile first.')

    if request.method == 'POST':
        help_option = request.form.get('help_option')
        if help_option:
            if help_option == 'Other':
                return redirect('/help_text')
            else:
                help_messages = [
    'Double-check your login credentials and ensure a stable internet connection to resolve access issues. If the problem persists, reach out to the website\'s support team for assistance.',
    'Clear your browser cache, close unnecessary tabs, and ensure a stable internet connection for better website performance. If the issue persists, try accessing the website from a different browser or device.',
    'Note down the error message and try refreshing the page. If the problem persists, contact the website\'s technical support for further assistance.',
    'Contact the website administrator or customer support to report the issue and provide specific details for them to rectify the inaccuracies or retrieve missing data.',
    'Check your internet connection and ensure you have the necessary permissions. Try using a different browser or device. If the problem persists, contact the website\'s support team for assistance.',
    'Verify that you have the proper access rights and try using a different browser or device. If the issue persists, contact the website\'s customer support for guidance on updating your personal information.',
    'Take your time to explore the website\'s layout and features. Look for user guides or tutorials provided by the website. If the interface remains confusing, provide feedback to the website\'s support team for improvement.',
    'Contact the website administrator or customer support and suggest implementing multilingual support to enhance accessibility for non-English speakers.',
    'Review the website\'s privacy policy, ensure the website is secure (https), and verify if it follows industry-standard data security practices. If you have specific concerns, contact the website administrator or support team for clarification.',
    'Follow any provided instructions on the website for scheduling or managing appointments. If you encounter difficulties, contact the website\'s customer support for assistance or consider reaching out to the healthcare provider directly.',
    'Document your inquiries and reach out to the website\'s customer support through their provided contact channels. If the response is inadequate, consider escalating the issue or seeking support from relevant regulatory bodies or consumer protection agencies.',
    'Try accessing the website from a different browser or device to see if the issue persists. Contact the website\'s support team for guidance on browser or device compatibility.',
    'Ensure you are using an up-to-date browser and check if there is a dedicated mobile app available for a better mobile experience. Provide feedback to the website\'s support team regarding the limited mobile functionality.',
    'Utilize the website\'s search functionality or navigation menu to locate the desired information. If you still struggle to find what you need, provide feedback to the website\'s support team for improvement.',
    'Check if you have the necessary permissions to access the images or test results. Ensure your browser and plugins are up to date. If the problem persists, contact the website\'s support team for assistance.',
    'Follow the instructions provided on the website for prescription refills or medication management. If you encounter issues, contact the website\'s customer support or consult your healthcare provider for guidance.',
    'Document the issues you are facing and contact the website\'s billing or insurance department directly for assistance. Be prepared to provide specific details and any relevant documentation.',
    'Check your notification settings within your account on the website. Ensure that the necessary permissions are granted and that your contact information is up to date. Contact the website\'s support team if the issue persists.',
    'Provide feedback to the website\'s support team regarding the need for more user-friendly self-care resources or educational materials. They may have additional resources or recommendations to address your specific needs.',
    'Contact the website administrator or customer support to inquire about their integration with EHR systems and request improvements or clarifications on how they handle EHR data integration.'
]


                solution = help_messages[int(help_option) - 1]
                return render_template('help.html', solution=solution)

    return render_template('help.html')


@app.route('/help_text', methods=['GET', 'POST'])
def help_text():
    user_id = session.get('user_id')  # Get the latest user ID from session

    if not user_id:
        return render_template('create_profile.html', message='Create your profile first.')

    if request.method == 'POST':
        text = request.form['text']
        if text:
            conn = sqlite3.connect(DATABASE2)
            c = conn.cursor()

            c.execute('''INSERT INTO help_text(user_id, name, text)
                         VALUES (?, ?, ?)''',
                      (user_id, session.get('full_name'), text))
            conn.commit()
            conn.close()

            return redirect('/')

    return render_template('help_text.html')
