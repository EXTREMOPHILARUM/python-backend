from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hello/<name>')
def hello(name):
    return render_template('Child.html', namechild=name)
