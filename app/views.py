from flask import render_template, flash, redirect
from app import app
from forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'Moo'}
    posts = [
        { 
            'author': { 'name': 'John' }, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': { 'name': 'Susan' }, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template('index.html', 
        title='Home',
        user=user,
        posts=posts)


@app.route('/login', method=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
        title='Sign In',
        form=form)