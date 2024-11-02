from flask import render_template, redirect, url_for, session, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from app.models import User, Post, Comment

def init_routes(app):
    # Move imports inside the function to avoid circular imports
    from app import db, login_manager, oauth

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Azure B2C configuration
   
    oauth.register(
        name='azure_b2c',
        client_id='', #AAA app reg client id 
         client_secret='', #AAA app reg client secret
        server_metadata_url='https://login.microsoftonline.com/te/te/v2.0/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

    @app.route('/')
    def home():
        posts = Post.query.all()
        return render_template('home.html', posts=posts)

    @app.route('/login')
    def login():
        redirect_uri = url_for('auth', _external=True)
        return oauth.azure_b2c.authorize_redirect(redirect_uri)

    @app.route('/auth')
    def auth():
        token = oauth.azure_b2c.authorize_access_token()
        user_info = oauth.azure_b2c.parse_id_token(token)

        user = User.query.filter_by(email=user_info['email']).first()
        if not user:
            user = User(email=user_info['email'])
            db.session.add(user)
            db.session.commit()

        login_user(user)
        return redirect(url_for('home'))

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))

    @app.route('/post', methods=['GET', 'POST'])
    @login_required
    def post_create():
        if request.method == 'POST':
            content = request.form['content']
            new_post = Post(content=content, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('home'))

        return render_template('post.html')

    @app.route('/post/<int:post_id>', methods=['GET', 'POST'])
    @login_required
    def post_detail(post_id):
        post = Post.query.get_or_404(post_id)
        if request.method == 'POST':
            content = request.form['content']
            new_comment = Comment(content=content, post_id=post.id, user_id=current_user.id)
            db.session.add(new_comment)
            db.session.commit()

        comments = Comment.query.filter_by(post_id=post.id).all()
        return render_template('post_detail.html', post=post, comments=comments)
