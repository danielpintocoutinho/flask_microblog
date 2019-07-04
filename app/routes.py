from app import app, db
from app.models import User
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm
from flask import flash, \
    redirect, \
    render_template, \
    url_for, \
    request
from flask_login import current_user, \
    login_user, \
    logout_user, \
    login_required


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The avengers movie was so cool'
        }
    ]

    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Dealing with strange case of the user already logged in
    # but being able to access login page.
    # current_user is a variable from Flask-Login that represents
    # the client of the request.
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # login_user from Flask-Login and registers the current_user variable
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        # url_parse.netloc determines if the path is relative to the domain
        # or absolute. If the latter, it would redirect to an external site
        # and could be dangerous. So, it redirects to the home page
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)