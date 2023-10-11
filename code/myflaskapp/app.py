from flask import Flask
from flask import render_template
from flask import request
from flask import url_for


app = Flask(__name__)

@app.route('/')
def home():
    return 'Home Page'

@app.route('/about')
def about():
    return 'About Page'

@app.route('/user/<username>')
def show_user_profile(username):
    return f'User {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'

@app.route('/hello/<name>')
def hello(name):
    return render_template('Child.html', namechild=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Logging in...'
    else:
        return 'Login Page'
    
    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    login_url = url_for('login')
    if request.method == 'POST':
        return 'Signing in...'
    else:
        return f'Signup Page <br> already signed up <a href={login_url}>Login</a>'
    
app.run(debug=True)