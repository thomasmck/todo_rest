from flask import Flask, abort, make_response, request
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

# Based on guide here: https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

@app.errorhandler(404)
def not_found(error):
    return make_response(json.dumps({'error': 'Not found'}), 404)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/todo', methods=['GET'])
def get_tasks():
    tasks = database_fetch("SELECT * FROM todolist")
    json_object = object_to_json(tasks)
    print(json_object)
    return json_object

@app.route('/todo/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = database_fetch("select * from todolist where id = %s" %task_id)
    if len(task) == 0:
        abort(404)
    json_object = object_to_json(task)
    print(json_object)
    return json_object

@app.route('/todo', methods=['POST'])
def post_task():
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

    # Fetch the result we just put
    task = database_fetch("SELECT * FROM todolist ORDER BY id DESC LIMIT 1;")
    json_object = object_to_json(task)
    return json_object

@app.route('/PUT/')
def put_task():
    pass

@app.route('/DELETE/')
def delete_task():
    pass

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
