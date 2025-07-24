from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'admin123'

sampleData = {
    "21A91A0501": {
        "name": "John Doe",
        "semesters": {
            1: [
                {
                    "code": "MA101",
                    "subject": "Mathematics-I",
                    "credits": 4,
                    "grade": "A"
                },
                {
                    "code": "PH101",
                    "subject": "Physics",
                    "credits": 3,
                    "grade": "B"
                },
                {
                    "code": "CH101",
                    "subject": "Chemistry",
                    "credits": 3,
                    "grade": "F"
                },
                {
                    "code": "EE101",
                    "subject": "Basic Electrical",
                    "credits": 3,
                    "grade": "B"
                },
                {
                    "code": "CS101",
                    "subject": "Programming in C",
                    "credits": 4,
                    "grade": "A"
                },
                {
                    "code": "EN101",
                    "subject": "English",
                    "credits": 2,
                    "grade": "A"
                },
            ],
            2: [
                {
                    "code": "MA201",
                    "subject": "Mathematics-II",
                    "credits": 4,
                    "grade": "A"
                },
                {
                    "code": "PH201",
                    "subject": "Physics-II",
                    "credits": 3,
                    "grade": "B"
                },
                {
                    "code": "ME201",
                    "subject": "Engineering Mechanics",
                    "credits": 3,
                    "grade": "A"
                },
                {
                    "code": "CS201",
                    "subject": "Data Structures",
                    "credits": 4,
                    "grade": "A"
                },
                {
                    "code": "EC201",
                    "subject": "Digital Electronics",
                    "credits": 3,
                    "grade": "B"
                },
            ],
        },
    },
    "21A91A0502": {
        "name": "Jane Smith",
        "semesters": {
            1: [
                {
                    "code": "MA101",
                    "subject": "Mathematics-I",
                    "credits": 4,
                    "grade": "A"
                },
                {
                    "code": "PH101",
                    "subject": "Physics",
                    "credits": 3,
                    "grade": "A"
                },
                {
                    "code": "CH101",
                    "subject": "Chemistry",
                    "credits": 3,
                    "grade": "F"
                },
                {
                    "code": "EE101",
                    "subject": "Basic Electrical",
                    "credits": 3,
                    "grade": "A"
                },
                {
                    "code": "CS101",
                    "subject": "Programming in C",
                    "credits": 4,
                    "grade": "A"
                },
                {
                    "code": "EN101",
                    "subject": "English",
                    "credits": 2,
                    "grade": "A"
                },
            ],
        },
    },
}


@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Simple hardcoded authentication - replace with real one
        if (username == 'admin'
                or username == 'admin@example.com') and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('admin_login'))

    return render_template('admin.html')


@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'):
        flash('Please log in to access the admin panel', 'error')
        return redirect(url_for('admin_login'))
    return render_template('adminpanel.html')


@app.route('/display', methods=['GET', 'POST'])
def display():
    if request.method == 'POST':
        rollno = request.form['rollno']
        sem = int(request.form['sem'])

        student = sampleData.get(rollno)
        semester_results = []
        student_name = None
        if student:
            student_name = student['name']
            semester_results = student['semesters'].get(sem, [])

        # ====== GPA and summary calculation STARTS here ======
        grade_points = {'A': 10, 'B': 8, 'C': 6, 'D': 4, 'F': 0}
        total_credits = sum(sub['credits'] for sub in semester_results)
        total_points = sum(sub['credits'] * grade_points.get(sub['grade'], 0)
                           for sub in semester_results)
        gpa = round(total_points /
                    total_credits, 2) if total_credits > 0 else 0.0
        total_subjects = len(semester_results)
        # ====== GPA and summary calculation ENDS here ========

        return render_template(
            'results.html',
            rollno=rollno,
            sem=sem,
            student_name=student_name,
            results=semester_results,
            total_credits=total_credits,
            gpa=gpa,
            total_subjects=total_subjects,
        )
    return render_template('results.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
