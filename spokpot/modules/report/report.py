from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"
@app.route("/hello")
def hello():
	return "hallao"
@app.route("/rama")
def rama():
	return "rama loh"
@app.route("/thiar")
def thiar():
	return "thi"

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
