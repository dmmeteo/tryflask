from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, login_required, current_user
from blog import app, db, login_manager, open_id
from blog.forms import LoginForm
from models import User, ROLE_ADMIN, ROLE_USER


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': {'name': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'name': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
@open_id.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        open_id.try_login(form.openid.data, ask_for=['name', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.before_request
def before_request():
    g.user = current_user


@open_id.after_login
def after_login(response):
    if response.email is None or response.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=response.email).first()
    if user is None:
        name = response.name
        if name is None or name == "":
            name = response.email.split('@')[0]
        user = User(name=name, email=response.email, role=ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))
