from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

socket_flask = SocketIO(app)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print(request)
        task_content = ""
        try:
            print(request)
            if request.is_json:
                print("im here 1")
                task = request.get_json()
                print(task)
                print("im here 5.1")



               # merged = name + ": " + word
                task_content = str(task) #merged
                #if program failed its over here
                susNameSt=task_content.index("'name':")
                susWordSt=task_content.index(", 'word':")
                susIP=task_content[(susNameSt+8):susWordSt]
                susWord=task_content[(susWordSt+10):-1]
                print(susIP)
                print(susWord)
                tryout=susIP+"=>"+susWord
                print(tryout)
                task_content=tryout
            else:
                try:
                    print("im here 2")
                   # print("im here 0")
                    print(request)
                    # print("yaya")
                    task_content = request.form['content']
                    # print(request.form['data'])
                    # task_content = 'request failed'
                except:
                    print("im here 3")
                    task_content = "failure"
        except:
            print("im here 5")
            task_content="failed"

        new_task = ToDo(content=task_content)
        print("added")
        try:
            db.session.add(new_task)
            db.session.commit()

            return redirect('/')
        except:
            return "There was an issue adding your task"
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/application/json', methods=['POST'])
def postJsonHandler():
    print(request.is_json)
    content = request.get_json()
    print(content)
    return 'JSON posted'


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()

        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = ToDo.query.get_or_404(id)

    if request.method == 'POST':
        try:
            task.content = request.form['content']


        except:
            task.content = "request failed"

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating that task'

    else:
        return render_template('update.html', task=task)


@socket_flask.on('message')
def handle_message(data):
    task_content = data.decode("utf-8")  # request.form['content']
    new_task = ToDo(content=task_content)
    print("added")
    try:
        db.session.add(new_task)
        db.session.commit()

        return redirect('/')
    except:
        return "There was an issue adding your task"


@socket_flask.on('connect', namespace='/web')
def connect_web():
    print("client connected!")


@socket_flask.on('disconnect', namespace='/web')
def disconnect_web():
    print("client disconnected!")


if __name__ == "__main__":
    app.run(debug=True, host="10.0.0.29")  # "10.0.0.26")
# socket_flask.run(app, host="10.0.0.43") # , host="10.0.0.37"
