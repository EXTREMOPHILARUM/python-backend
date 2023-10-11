from flask import Flask
from flask import request
from flask import render_template, flash, redirect, url_for

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "iwoenrqksdnvc@@v93nb"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
login_manager = LoginManager(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Signup")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ResetPasswordForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    newpassword = PasswordField("New Password", validators=[DataRequired()])
    submit = SubmitField("Reset")


class DeleteUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Delete")


@app.route("/")
def home():
    return "Home Page"


@app.route("/about")
def about():
    return "About Page"


@app.route("/user/<username>")
def show_user_profile(username):
    return f"User {username}"


@app.route("/post/<int:post_id>")
@login_required
def show_post(post_id):
    return f"Post {post_id}"


@app.route("/hello/<name>")
def hello(name):
    return render_template("Child.html", namechild=name)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(
            "Login requested for user {}, remember_me={}".format(
                form.username.data, form.password.data
            )
        )
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.password == form.password.data:
                login_user(user)
                return "User successfully logged in"
            else:
                return "Wrong password"
        else:
            return Exception("Invalid username or password")
        return redirect(url_for("home"))
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/resetpass", methods=["GET", "POST"])
def resetpass():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        print(
            f"Password reset requested for user {form.username.data}, password={form.password.data}"
        )
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.password == form.password.data:
                user.password = form.newpassword.data
                db.session.commit()
                return "User Password changed successfully"
            else:
                return "Wrong password"
        else:
            return "User not found"
        return redirect(url_for("home"))
    return render_template("resetpass.html", form=form)


@app.route("/deleteuser", methods=["GET", "POST"])
@login_required
def deleteuser():
    form = DeleteUserForm()
    if form.validate_on_submit():
        print(
            f"Password reset requested for user {form.username.data}, password={form.password.data}"
        )
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.password == form.password.data:
                db.session.delete(user)
                db.session.commit()
                return "User delete successfully"
            else:
                return "Wrong password"
        else:
            return "User not found"
        return redirect(url_for("home"))
    return render_template("deleteuser.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    db.create_all()
    if form.validate_on_submit():
        print(
            f"Signup requested for user {form.username.data}, password={form.password.data}"
        )
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("signup.html", form=form)


# app.run(
#     debug=True
# )
