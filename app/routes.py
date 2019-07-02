from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Daniel'}
    
    posts = [
        {
            'author': 'John',
            'body': 'Beautiful day in Portland'
        },
        {
            'author':  'Susan',
            'body': 'The avengers movie was so cool'
        }
    ]

    return render_template('index.html', title='Home', user=user, posts=posts)