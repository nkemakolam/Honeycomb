from flask import Flask, jsonify, render_template, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import cross_origin
from authlib.integrations.flask_client import OAuth
from functools import wraps
import os

app = Flask(__name__)
app.secret_key ='68d624de4f80d19dfe54c01db056f71ce88b693c00e7e8c06b12df328bf13a43'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Auth0 Configuration
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id='vmaIlniUIDBIQmFJJteV9X2toinaa3NA',
    client_secret='MRtJek_Er6SweRSaQsV2rOoWi5sOUoIJBhcpT90lyEMFlCpF5hVG0VVrnh5cmEQ6',
     client_kwargs={
         'scope': 'openid profile email',
     },
     server_metadata_url=f'https://cybercare.auth0.com/.well-known/openid-configuration'
)




class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user = db.Column(db.String(100), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)
    likes = db.Column(db.Integer, default=0)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    user = db.Column(db.String(100), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


# Authentication
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

    #return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=url_for('callback', _external=True))


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token

    # session['profile'] = {
    #     'user_id': userinfo['sub'],
    #     'name': userinfo['name'],
    #     'email': userinfo['email']
    # }

    return redirect('/')
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@requires_auth
def view_post(post_id):
    post = Post.query.get(post_id)
    if request.method == 'POST':
        comment_body = request.form.get('comment')
        new_comment = Comment(body=comment_body, user=session['profile']['name'], post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
    return render_template('post.html', post=post)


@app.route('/like/<int:post_id>')
@requires_auth
def like_post(post_id):
    post = Post.query.get(post_id)
    post.likes += 1
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/create', methods=['GET', 'POST'])
@requires_auth
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        new_post = Post(title=title, body=body, user=session['profile']['name'])
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')
    return render_template('create.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000, debug=True)
