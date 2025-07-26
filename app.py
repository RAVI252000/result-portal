from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import PrimaryKeyConstraint
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/result_portal"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'admin123'


class Result(db.Model):
    __tablename__ = 'results'

    Rollno = db.Column(db.String(10))
    Sub_Code = db.Column(db.String(7))
    Semester = db.Column(db.Integer)
    Name = db.Column(db.String(40), nullable=False)
    Sub_Name = db.Column(db.String(10), nullable=False)
    Credits = db.Column(db.Integer, nullable=False)
    Grade = db.Column(db.String(1), nullable=False)

    # No primary key
    __mapper_args__ = {
        'primary_key':
        [Rollno, Sub_Code,
         Semester]  # still required internally unless truly no key
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
    total_students = db.session.query(Result.Rollno).distinct().count()
    total_results = Result.query.count()
    return render_template('adminpanel.html',
                           total_students=total_students,
                           total_results=total_results)


@app.route('/display', methods=['GET', 'POST'])
def display():
    if request.method == 'POST':
        rollno = request.form['rollno']
        sem = int(request.form['sem'])

        results = Result.query.filter_by(Rollno=rollno, Semester=sem).all()

        if not results:
            student_name = None
            semester_results = []
        else:
            student_name = results[0].Name
            semester_results = [{
                "code": r.Sub_Code,
                "subject": r.Sub_Name,
                "credits": r.Credits,
                "grade": r.Grade,
            } for r in results]

        grade_points = {'A': 10, 'B': 8, 'C': 6, 'D': 4, 'F': 0}
        total_credits = sum(sub['credits'] for sub in semester_results)
        total_points = sum(sub['credits'] * grade_points.get(sub['grade'], 0)
                           for sub in semester_results)
        gpa = round(total_points /
                    total_credits, 2) if total_credits > 0 else 0.0
        total_subjects = len(semester_results)

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


@app.route('/upload_results', methods=['POST'])
def upload_results():
    exam_type = request.form.get('exam_type')
    semester = int(request.form.get('semester'))
    file = request.files['result_file']

    if file and file.filename != '':
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(filepath)

        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(filepath)
            elif filename.endswith('.xlsx'):
                df = pd.read_excel(filepath)
            else:
                flash('Unsupported file type.', 'error')
                return redirect(url_for('admin_panel'))

            # Loop through and insert/update database
            for _, row in df.iterrows():
                result = Result.query.filter_by(Rollno=row['Rollno'],
                                                Sub_Code=row['Sub_Code'],
                                                Semester=semester).first()

                if result:
                    # Update existing record
                    result.Name = row['Name']
                    result.Sub_Name = row['Sub_Name']
                    result.Credits = int(row['Credits'])
                    result.Grade = row['Grade']
                else:
                    # Insert new record
                    new_result = Result(Rollno=row['Rollno'],
                                        Sub_Code=row['Sub_Code'],
                                        Semester=semester,
                                        Name=row['Name'],
                                        Sub_Name=row['Sub_Name'],
                                        Credits=int(row['Credits']),
                                        Grade=row['Grade'])
                    db.session.add(new_result)

            db.session.commit()
            flash(
                f'{exam_type} results uploaded successfully for Semester {semester}.',
                'success')

        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'error')

        # Optional: remove file after processing
        os.remove(filepath)

    else:
        flash('No file uploaded.', 'error')

    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
