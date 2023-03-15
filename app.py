from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import json 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/todo_db'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(150))
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}>'


@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_data = {}
        task_data['id'] = task.id
        task_data['title'] = task.title
        task_data['description'] = task.description
        task_data['done'] = task.done
        task_list.append(task_data)
    json_data = json.dumps({'tasks': task_list}, ensure_ascii=False).encode('utf8')
    response = make_response(json_data)
    response.headers['Content-Type'] = 'application/json;charset=utf-8'
    return response


@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data['title']
    description = data.get('description', '')
    done = data.get('done', False)
    new_task = Task(title=title, description=description, done=done)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'New task created!'})



@app.route('/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'PUT':
        data = request.get_json()
        task.title = data['title']
        task.description = data.get('description', '')
        task.done = data.get('done', False)
        db.session.commit()
        return jsonify({'message': 'Task updated!'})
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted!'})


if __name__ == '__main__':
    app.run(debug=True)
