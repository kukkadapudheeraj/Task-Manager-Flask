from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskmanager.db'
db = SQLAlchemy(app)

class TaskManager(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)


    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/',methods=['GET','POST'])
def index():

    if request.method == 'POST':
        task_content = request.form['content']
        new_task = TaskManager(content=task_content)

        try:    
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error in adding task'
    else:

        tasks = TaskManager.query.order_by(TaskManager.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = TaskManager.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return  'Issue in deleting task'


@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task_to_update = TaskManager.query.get_or_404(id)
    if request.method == 'POST':
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue in updating task'
    else:
        return render_template('update.html',task=task_to_update)

if __name__ == "__main__":
    app.run(debug=True)