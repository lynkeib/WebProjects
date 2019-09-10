from flask import Flask, request
from flask import flash, redirect, url_for, render_template, session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/<name>')
def index(name):
    return render_template('index.html',name=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != 'shiyanlou' or request.form['password'] != 'shiyanlou':
            flash('username or password invalid')
            return redirect(url_for('index', name='world'))
        else:
            session['username'] = request.form['username']
            name = request.form['username']
            flash('you were logged in')
            return redirect(url_for('index', name=name))
    return render_template('login.html')