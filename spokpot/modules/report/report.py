import jinja2
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, g, render_template, request, session, redirect, url_for
from functools import wraps

app = Flask(__name__)

DATABASE = 'glastopf.db'
app.secret_key = 'A49c,1050szd1295*&0l4l&'
PER_PAGE = 20


@app.after_request
def add_header(response):
	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers['Cache-Control'] = 'public, max-age=0'
	return response

# decorator login required
def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if 'username' not in session:
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorated_function

# pagination
def url_for_other_page(page):
	args = request.view_args.copy()
	args['page'] = page
	return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


# Routing
@app.route('/')
@login_required
def index():
	events = query_db('select * from events where pattern = "lfi" limit 3 ')
	menu = 'Dashboard'
	return render_template('dashboard.html', events=events, menu=menu)

@app.route('/login', methods=['POST', 'GET'])
def login():
	error = None
	if request.method == 'POST':
		if(request.form['username'] == 'aldo' and request.form['password'] == 'aldo'):
			session['username'] = 'aldo'
			return redirect(url_for('index'))
		else:
			error = 'Invalid username/password'
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))

@app.route('/data', defaults={'page': 1})
@app.route('/data/<int:page>')
@login_required
def data(page):
	total = query_db('select count(*) from events')
	menu = 'Data'
	events = query_db('select * from events limit 20 ')
	return render_template('data.html', events=events, menu=menu)



# database
def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
		db.row_factory = make_dicts
	return db

def make_dicts(cursor, row):
	return dict((cursor.description[idx][0], value)
		for idx, value in enumerate(row))


def close_connection():
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv


if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0')
