import jinja2
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, g, render_template, request, session, redirect, url_for, abort
from functools import wraps
from pagination import Pagination
app = Flask(__name__)

DATABASE = 'spokpot.db'
app.secret_key = 'A49c,1050szd1295*&0l4l&'
PER_PAGE = 20


#####################################################
#													#
#				 Flask Related 						#
#													#
#####################################################

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

#####################################################
#													#
#					  Routing 						#
#													#
#####################################################
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

@app.route('/data/', defaults={'page': 1})
@app.route('/data/<int:page>')
@login_required
def data(page=None,type=None):
	total = int(query_db('select count(*) as total from events', one=True)['total'])
	menu = 'Data'
	ceil = total / PER_PAGE
	sqlpage = page * PER_PAGE - (PER_PAGE + 1)
	events = query_db('select * from events limit '+ str(sqlpage) +', 20 ')
	if not events and page != 1:
		return '404'
	pagination = Pagination(page, PER_PAGE, total)

	return render_template('data.html', events=events, pagination=pagination, menu=menu)

@app.route('/data/<type>/', defaults={'page': 1})
@app.route('/data/<type>/<int:page>')
def data_type(type=None,page=None):
	total = int(query_db('select count(*) as total from events where pattern = ?',[type], one=True)['total'])
	menu = 'Data by'
	ceil = total / PER_PAGE
	sqlpage = page * PER_PAGE - (PER_PAGE + 1)
	events = query_db('select * from events where pattern = ? limit '+ str(sqlpage) +', 20 ',[type])
	if not events and page != 1:
		return '404'
	pagination = Pagination(page, PER_PAGE, total)

	return render_template('data.html', events=events, pagination=pagination, menu=menu)

@app.route('/chart')
@app.route('/chart/<type>')
def chart(type=None):
	menu = 'Chart'
	bydate = query_db("select count(*) as sum, strftime('%H:%M %d-%m', time) as date  from events group by strftime('%M', time) ")
	bypattern = query_db("select count(*) as sum, pattern from events where pattern != 'unknown' group by pattern ")
	for pattern in bypattern:
		pattern['color'] = '#F38630'
	byip = query_db("select count(*) as sum, strftime('%d-%m', time) date  from events group by strftime('%H', time) ")
	return render_template('chart.html', menu=menu, bydate=bydate,bypattern=bypattern, type=type)

@app.route('/attack')
@app.route('/attack/<id>')
@login_required
def attack(id):
	event = query_db("select * from events where id = ?", [id], one=True)
	menu = 'Attack'
	return render_template('attack.html', menu=menu, event=event)

#####################################################
#													#
#					  Database 						#
#													#
#####################################################
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

#####################################################
#													#
#				 Fungsi lain 						#
#													#
#####################################################


if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0')
