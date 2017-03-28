from flask import Flask, jsonify
app = Flask(__name__)
mytasks = [
{
'id': 1,
'task': u'Finish Hello World',
'session': u'Week 7',
'done': True
},

{
'id': 2,
'task': u'Finish first API',
'session': u'Week 7',
'done': False
}
]
@app.route('/todo/api/tasks', methods=['GET'])
def get tasks():
return jsonify({'tasks': mytasks})
