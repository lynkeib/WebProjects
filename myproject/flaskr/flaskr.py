import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

# Set variables
DATABASE = '/tmp/flaskr.db'
ENV = 'development'
DEBUG = 1
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'

# Start App
app = Flask(__name__)
app.config.from_object(__name__)

# Connect to Database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
## Initiate Dadabase
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read().decode())
        db.commit()

## Initiate the connection before the request
@app.before_request
def before_request():
    g.db = connect_db()

## Close the connection after the request
@app.teardown_request
def teardown_request(exception):
    g.db.close()

## Query from the Database and show the entries
@app.route('/')
def show_entries():
    data = g.db.execute('select title, text from entries order by id desc') 
    entries = [{'title':row[0], 'text':row[1]} for row in data.fetchall()]
    return render_template('show_entries.html', entries=entries)

## Add new entry
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',[request.form['title'], request.form['text']])
    g.db.commit()
    flash('You just posted a new entry')
    return redirect(url_for('show_entries'))

## Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:  
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:   
            error = 'Invalid password'
        else:
            session['logged_in'] = True  
            flash('You were logged in')   
            return redirect(url_for('show_entries'))   
    return render_template('login.html', error=error)

## Logout
@app.route('/logout')
def logout():
	session['logged_in'] = False
	# session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

## Main ##
if __name__ == '__main__':
    app.run()