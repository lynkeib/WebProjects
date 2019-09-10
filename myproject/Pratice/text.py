from flask import Flask 
app= Flask(__name__)

@app.route('/')
def index():
	return "index page"

@app.route('/home')
def hello_word():
	return "hello world"

@app.route('/user/<username>')
def show_user_profile(username):
	# show user name
	return f"User :{username}"

@app.route("/post/<int:post_id>")
def show_post(post_id):
	return f"Post {post_id}"

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
	return f"subpath {subpath}"

@app.route('/projects/')
def projects():
	return "This is project page"

@app.route('/about')
def anout():
	return "the about page"