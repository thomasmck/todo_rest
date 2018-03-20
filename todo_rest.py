from flask import Flask, abort, make_response, request, jsonify
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

# Based on guide here: https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

@app.errorhandler(404)
def not_found(error):
    return make_response(json.dumps({'error': 'Not found'}), 404)

@app.route('/todo', methods=['GET'])
def get_tasks():
    # Return all tasks
    tasks = database_fetch("SELECT * FROM todolist")
    json_object = object_to_json(tasks)
    print(json_object)
    return json_object

@app.route('/todo/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # Return a specific (by id) task
    task = database_fetch("select * from todolist where id = %s" %task_id)
    if len(task) == 0:
        abort(404)
    json_object = object_to_json(task)
    print(json_object)
    return json_object

@app.route('/todo', methods=['POST'])
def post_task():
    # Creates a new task
    # curl -H "Content-Type: application/json" -X POST -d '{"title":"Read a book", "description":"test curl"}' http://localhost:5000/todo

    if not request.json or not 'title' in request.json:
        abort(400)
    date = datetime.now()
    title = request.json['title']
    description = request.json.get('description', "")
    done = False
    # This is super ugly, should be converted to some sort of wrapper
    command = "INSERT INTO todolist (date, title, description, done) VALUES (\'%s\', \'%s\', \'%s\', \'%s\')" %(date, title, description, done)
    database_put(command)

    # Fetch the result we just created
    task = database_fetch("SELECT * FROM todolist ORDER BY id DESC LIMIT 1;")
    json_object = object_to_json(task)
    return json_object

@app.route('/todo/<int:task_id>', methods=['PUT'])
def put_task(task_id):
    # Updates details for an existing task
    #  curl -H "Content-Type: application/json" -X PUT -d '{"title":"Updated1", "description":"Updated1"}' http://localhost:5000/todo/2
    task = database_fetch("select * from todolist where id = %s" % task_id)
    # Check input meets requirements
    if len(task) == 0:
        abort(404)
    task = task[0]
    if not request.json:
        abort(400)
    """ if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)"""
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    title = request.json.get('title', task[1])
    description = request.json.get('description', task[2])
    done = request.json.get('done', task[3])
    command = "UPDATE todolist SET title = \'%s\', description = \'%s\', done = \'%s\' WHERE id = %s" %(title, description, done, task_id)
    database_put(command)

    # Fetch the updated task
    task = task = database_fetch("select * from todolist where id = %s" % task_id)
    json_object = object_to_json(task)
    return json_object

@app.route('/todo/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = database_fetch("select * from todolist where id = %s" % task_id)
    # Check input meets requirements
    if len(task) == 0:
        abort(404)
    command = "DELETE FROM todolist WHERE id = %s" % task_id
    database_put(command)
    return jsonify({'result': True})

def object_to_json(objects):
    # Convert database entries to json format
    list = []
    for object in objects:
        object_dict = {
            'date': object[0],
            'title': object[1],
            'description': object[2],
            'done': object[3]
        }
        list.append(object_dict)
    if len(list) == 1:
        list = list[0]
    dictionary = {'task': list}
    return json.dumps(dictionary)

def database_put(command):
    c, conn = database_connect()
    c.execute(command)
    conn.commit()
    conn.close()

def database_fetch(command):
    # From command line specifying ./sqlite3.db worked, did not work here though
    c, conn = database_connect()
    c.execute(command)
    data = c.fetchall()
    conn.close()
    return data

# Looks like flask has some nicer ways of handling db connections: http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
# Should consider using these instead
def database_connect():
    conn = sqlite3.connect("C:\\Users\\Tom\\Documents\\git_repos\\todo_rest\\sqlite3.db")
    c = conn.cursor()
    return c, conn

if __name__ == '__main__':

    # Table format
    # todolist(date DATE, title TEXT, description TEXT, done BOOL)
    app.run()
