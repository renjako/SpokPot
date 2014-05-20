from sqlite3 import dbapi2 as sqlite3
from flask import Flask, g
app = Flask(__name__)

DATABASE = 'glastopf.db'


@app.route("/")
def index():
	# db = get_db()
	# curr = db.execute("select * from events where id = 1")
	# entries  = curr.fetchall()
	result = ''
	for events in query_db('select * from events where id = 1'):
		print(events[0], 'has the id', events[1])
		result += str(events[0]) +' '+ events[1] +' '+ events[2] +' '+' '+ events[3] +' '+ events[4] +' '+ events[5] +'<br/>'
	return result

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db

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
