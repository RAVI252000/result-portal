from flask import Flask, render_template, request

app = Flask(__name__)

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


@app.route('/admin/login')
def admin():
    return render_template('admin.html')


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
