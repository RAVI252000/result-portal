from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
  return render_template('homepage.html')


@app.route('/display', methods=['GET', 'POST'])
def display():
  if request.method == 'POST':
    rollno = request.form['rollno']
    sem = request.form['sem']
    # Fetch result data for rollno and sem, then pass it to results.html
    # For demonstration, just pass rollno and sem:
    return render_template('results.html', rollno=rollno, sem=sem)
  return render_template('results.html')  # optional for GET


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
