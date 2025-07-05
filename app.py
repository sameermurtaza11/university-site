# from os import name
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

ALLOWED_ADMIN_IPS = ['127.0.0.1', '192.168.1.100']  # Example secure IPs

@app.before_request
def restrict_login():
    # Only restrict login page, not other endpoints
    if request.endpoint == 'login' and request.remote_addr not in ALLOWED_ADMIN_IPS:
        return "Access denied: Unauthorized IP", 403

PROGRAMS = [
    {
        'id': 1,
        'title': 'MS in Nuclear Engineering',
        'duration': '2 Years',
        'eligibility': 'BSc Physics or Engg',
        'category': 'MS',
        'curriculum': 'Advanced Nuclear Physics, Reactor Design, Radiation Safety',
        'outcomes': 'Research, Industry, Government roles',
        'brochure_url': '/static/files/ms_brochure.pdf'
    },
    {
        'id': 2,
        'title': 'Post Diploma Training Programme (PDTP)',
        'duration': '1 Year',
        'eligibility': 'DAE or BSc',
        'category': 'PDTP',
        'curriculum': 'Nuclear Plant Operations, Safety, Instrumentation',
        'outcomes': 'Plant Operator, Technician',
        'brochure_url': '/static/files/pdtp_brochure.pdf'
    },
    {
        'id': 3,
        'title': 'Post Graduate Training Programme (PGTP)',
        'duration': '1 Year',
        'eligibility': 'BSc Engineering',
        'category': 'PGTP',
        'curriculum': 'Nuclear Systems, Control, Safety',
        'outcomes': 'Junior Engineer, Safety Officer',
        'brochure_url': '/static/files/pgtp_brochure.pdf'
    },
    # Add more programs
]

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'  # Replace with a secure password in production

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USERNAME and request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_programs'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/programs/<int:program_id>')
def program_detail(program_id):
    program = next((p for p in PROGRAMS if p['id'] == program_id), None)
    if not program:
        return "Program not found", 404
    return render_template('program_detail.html', program=program)

@app.route('/admin/programs', methods=['GET', 'POST'])
def admin_programs():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # You can render a template or return a message
    return render_template('program_admin.html')

@app.route('/programs')
def programs():
    category = request.args.get('category', 'All')
    if category and category != 'All':
        filtered_programs = [p for p in PROGRAMS if p.get('category', '').lower() == category.lower()]
    else:
        filtered_programs = PROGRAMS
    return render_template('program_grid.html', programs=filtered_programs, selected_category=category or 'All')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apply/<int:program_id>', methods=['GET', 'POST'])
def apply(program_id):
    # Logic for applying to the program
    return render_template('apply.html', program_id=program_id)

FACULTY = [
    {
        'name': 'Dr. A. Example',
        'title': 'Professor & Head of Department',
        'qualifications': 'PhD, Nuclear Engineering',
        'email': 'a.example@kinpoe.edu.pk',
        'photo': ''
    },
    {
        'name': 'Dr. B. Example',
        'title': 'Associate Professor',
        'qualifications': 'PhD, Radiation Protection',
        'email': 'b.example@kinpoe.edu.pk',
        'photo': ''
    },
    {
        'name': 'Dr. C. Example',
        'title': 'Assistant Professor',
        'qualifications': 'PhD, Medical Physics',
        'email': 'c.example@kinpoe.edu.pk',
        'photo': ''
    },
    {
        'name': 'Dr. D. Example',
        'title': 'Lecturer',
        'qualifications': 'MPhil, Nuclear Materials',
        'email': 'd.example@kinpoe.edu.pk',
        'photo': ''
    },
    {
        'name': 'Dr. E. Example',
        'title': 'Senior Lecturer',
        'qualifications': 'PhD, Reactor Physics',
        'email': 'e.example@kinpoe.edu.pk',
        'photo': ''
    },
    {
        'name': 'Dr. F. Example',
        'title': 'Professor',
        'qualifications': 'PhD, Nuclear Chemistry',
        'email': 'f.example@kinpoe.edu.pk',
        'photo': ''
    },
    {
        'name': 'Dr. G. Example',
        'title': 'Assistant Professor',
        'qualifications': 'PhD, Health Physics',
        'email': 'g.example@kinpoe.edu.pk',
        'photo': ''
    },
    {
        'name': 'Dr. H. Example',
        'title': 'Lecturer',
        'qualifications': 'MPhil, Nuclear Safety',
        'email': 'h.example@kinpoe.edu.pk',
        'photo': ''
    },
    {
        'name': 'Dr. I. Example',
        'title': 'Associate Professor',
        'qualifications': 'PhD, Nuclear Instrumentation',
        'email': 'i.example@kinpoe.edu.pk',
        'photo': ''
    },
    {
        'name': 'Dr. J. Example',
        'title': 'Professor',
        'qualifications': 'PhD, Nuclear Policy',
        'email': 'j.example@kinpoe.edu.pk',
        'photo': ''
    },
]

@app.route('/faculty')
def faculty():
    return render_template('includes/faculty.html')

@app.route('/qec')
def qec():
    return render_template('includes/qec.html')

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/about')
def about():
    return render_template('about.html', faculty=FACULTY)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # You can add email sending logic here if needed
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
