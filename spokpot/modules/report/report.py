import jinja2
import os
import sys
import random
from html.parser import HTMLParser as parser
from sqlite3 import dbapi2 as sqlite3
from datetime import datetime
from flask import Flask, g, render_template, request, session, redirect, url_for, abort
from functools import wraps
from pagination import Pagination


sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from modules.database.sqlite import init_db, db_session
from modules.models.event import Event

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

# paginationd
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
	now = datetime.now().strftime('%Y-%m-%d')
	now = now+"%"
	events = query_db("select count(*) as sum, pattern from events where pattern != 'favicon' and pattern != 'unknown' and pattern != 'robot' and pattern != 'style_css' and  time like '" + now + "' group by pattern ")
	# events = query_db("select count(*) as sum, pattern from events where pattern != 'favicon' and pattern != 'unknown' and pattern != 'robot' and pattern != 'style_css' and  time like '2014-06-25%' group by pattern ")
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


@app.route('/line/')
@app.route('/line/<type>')
def line(type=None):
	# all by date
	menu = 'Line Chart'
	# bydate = query_db("select count(*) as sum, strftime('%d-%m', time) as date  from events group by strftime('%d', time) order by time ")
	if type != None:
		bydate = query_db("select count(*) as sum, strftime('%d-%m', time) as date from events where pattern = ? group by strftime('%d', time) order by time ", [type])
		events = query_db("select * from events where pattern = ? order by id desc limit 10 ",[type])
	else:
		bydate = query_db("select count(*) as sum, strftime('%d-%m', time) as date from events group by strftime('%d', time) order by time ")
		events = query_db("select * from events order by id desc limit 10 ")
	for event in events:
		event['request_raw'] = event['request_raw'].split(' ')[0]
	pattern = query_db("select pattern from events group by pattern order by pattern")
	byip = query_db("select count(*) as sum, strftime('%d-%m', time) date  from events group by strftime('%H', time) ")
	return render_template('line.html', menu=menu, bydate=bydate, pattern=pattern, type=type, events=events)

@app.route('/pie/')
@app.route('/pie/<type>')
def pie(type=None):
	menu = 'Pie Chart'
	pattern = query_db("select pattern from events group by pattern order by pattern")
	if type != 'ip':
		bypattern = query_db("select count(*) as sum, pattern from events where pattern != 'unknown' and pattern != 'favicon' and pattern != 'style_css' group by pattern order by sum desc")
	else:
		bypattern = query_db("select count(*) as sum, source as pattern from events group by source order by sum desc")
	for byp in bypattern:
		byp['color'] = "#%06x" % random.randint(0,0xFFFFFF)
	byip = query_db("select count(*) as sum, source from events group by source ")
	return render_template('pie.html', menu=menu, pattern=pattern, bypattern=bypattern, type=type)

@app.route('/request', defaults={'page': 1})
@app.route('/request/<int:page>')
@login_required
def request_url(page=None):
	total = int(query_db('select count(*) as total from events group by request_url', one=True)['total'])
	menu = 'Request'
	ceil = total / PER_PAGE
	sqlpage = page * PER_PAGE - (PER_PAGE + 1)
	events = query_db("select id, count(*) as total, request_url from events where pattern = 'unknown' group by request_url order by total desc limit "+ str(sqlpage) +", 20 ")
	if not events and page != 1:
		return '404'
	pagination = Pagination(page, PER_PAGE, total)

	return render_template('request.html', events=events, pagination=pagination, menu=menu)

@app.route('/data/', defaults={'page': 1})
@app.route('/data/<int:page>')
@login_required
def data(page=None,type=None):
	total = int(query_db('select count(*) as total from events', one=True)['total'])
	menu = 'Data'
	ceil = total / PER_PAGE
	sqlpage = page * PER_PAGE - PER_PAGE
	events = query_db('select * from events limit '+ str(sqlpage) +', 20 ')
	for event in events:
		event['request_raw'] = event['request_raw'].split(' ')[0]	
	if not events and page != 1:
		return '404'
	pattern = query_db("select pattern from events group by pattern order by pattern")
	pagination = Pagination(page, PER_PAGE, total)
	return render_template('data.html', events=events, pagination=pagination, pattern=pattern, menu=menu)

@app.route('/data/<type>/', defaults={'page': 1})
@app.route('/data/<type>/<int:page>')
def data_type(type=None,page=None):
	total = int(query_db('select count(*) as total from events where pattern = ?',[type], one=True)['total'])
	menu = 'Data by'
	ceil = total / PER_PAGE
	sqlpage = page * PER_PAGE - (PER_PAGE + 1)
	events = query_db("select * from events where pattern = ? limit "+ str(sqlpage) +", 20 ",[type])
	for event in events:
		event['request_raw'] = event['request_raw'].split(' ')[0]
	if not events and page != 1:
		return '404'
	pattern = query_db("select pattern from events group by pattern order by pattern")
	pagination = Pagination(page, PER_PAGE, total)
	return render_template('data.html', events=events, pagination=pagination, pattern=pattern, type=type, menu=menu)

@app.route('/attack')
@app.route('/attack/<id>')
@login_required
def attack(id):
	event = query_db("select * from events where id = ?", [id], one=True)
	# for attack in event:

	breakline = '<br />'
	event['request_raw'] = event['request_raw'].replace('\n', breakline)
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
