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
    return render_template('program_grid.html', programs=PROGRAMS, selected_category='All')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apply/<int:program_id>', methods=['GET', 'POST'])
def apply(program_id):
    # Logic for applying to the program
    return render_template('apply.html', program_id=program_id)

if __name__ == '__main__':
    app.run(debug=True)
