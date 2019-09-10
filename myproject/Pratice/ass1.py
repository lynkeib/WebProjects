from flask import Flask
app = Flask(__name__)

@app.route('/<path:username>')
def username(username):
	return f"this is user {username}"

@app.route('/sum/<int:a>/<int:b>')
def sum(a, b):
	return f"sum is {a + b}"