from flask import Flask, render_template, request, url_for, redirect

#ORM - object-oriented model
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)


class Students(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), nullable = False)
    def __str__(self):
        return f'<Student {self.name}>'

    def __repr__(self):
        return f'<Student {self.id} - {self.name}>'



@app.route('/students/')
def index():
    students = Students.query.all()

    return render_template('index.html', students=students)


@app.route('/students/<int:student_id>/')
def get_student_info(student_id):
    student = Students.query.get_or_404(student_id)
    return student.name

@app.route('/students/create/', method = ('GET', 'POST'))
def student_create():
    if request.method == 'POST':
        #filling params
        name = request.form['name']

        #create instance
        stud = Students(
            name = name
        )

        #add to session db
        db.session.add(stud)

        #db commiting ( apply changes )
        db.session.commit()

        return (url_for('students'))

    return render_template('create_student.html')
