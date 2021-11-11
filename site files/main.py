# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for 
from database import db
from models import Post as Post
from models import User as User
app = Flask(__name__)     # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)
# Setup models
with app.app_context():
    db.create_all()   # run under the app context

#Posts = {1:{'title': 'First post', 'text': 'This is my first post','date': '10-19-2021'},
#    2:{'title': 'Second post', 'text': 'This is my second post','date': '10-19-2021'},
#   3:{'title': 'Third post', 'text': ' This is my third post','date': '10-19-2021'},
#   }
# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
def index():
    a_user =  db.session.query(User).filter_by(email='placeholder@uncc.edu').one()
    return render_template('index.html')
@app.route('/posts')
def get_posts():
    a_user = db.session.query(User).filter_by(email='placeholder@uncc.edu').one()
    my_posts = db.session.query(Post).all()
    return render_template('posts.html', posts=my_posts)
@app.route('/posts/<post_id>')
def get_post(post_id):
    a_user = db.session.query(User).filter_by(email='placeholder@uncc.edu').one()
    my_post = db.session.query(Post).filter_by(id=post_id).one()
    return render_template('post.html', post=my_post)
@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():

    print('request method is', request.method)
    if request.method == 'POST':
        #title data
        title = request.form['title']
        #note data
        text = request.form['postText']
        #date stamp
        from datetime import date
        today = date.today()
        #format date
        today = today.strftime("%m-%d-%Y")
        new_record = Post(title, text, today)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('get_posts'))
    else:
        a_user = db.session.query(User).filter_by(email='placeholder@uncc.edu').one()
        return render_template('new.html', user = a_user)
@app.route('/posts/edit/<post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['postText']
        post = db.session.query(Post).filter_by(id=post_id).one()
        post.title = title
        post.text = text
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('get_posts'))
    else:
        a_user = db.session.query(User).filter_by(email='placeholder@uncc.edu').one()
        my_post = db.session.query(Post).filter_by(id=post_id).one()
        return render_template('new.html', post=my_post, user=a_user)
@app.route('/posts/delete/<post_id>', methods=['POST'])
def delete_post(post_id):
    #retrieve the post from the db
    my_post = db.session.query(Post).filter_by(id=post_id).one()
    db.session.delete(my_post)
    db.session.commit()
    return redirect(url_for('get_posts'))
    
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.