from flask import render_template, redirect, flash, url_for
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import posts, User, Post


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title="About")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}", "success")
        return redirect(url_for('home'))

    return render_template('register.html', title="Registration", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "test@test.com" and form.password.data == "password":
            flash("You have been logged in", "success")
            return redirect(url_for('home'))
        else:
            flash("Please check your email and password", 'danger')

    return render_template('login.html', title="Sign In", form=form)
