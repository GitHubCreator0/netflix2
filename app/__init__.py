from flask import Flask, render_template, redirect, request
from .forms import RegistrationForm, LoginForm, PostForm, CommentForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required, current_user
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '12342'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
app.app_context().push()

login.login_view = 'login'

@login.user_loader
def user_loader(id):
    return Admin.query.get(int(id))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    post = db.Column(db.Integer, db.ForeignKey('preview.id'))


class MovieComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    post = db.Column(db.Integer, db.ForeignKey('movie.id'))


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


class Preview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    image = db.Column(db.String)
    user = db.Column(db.Integer, db.ForeignKey('admin.id'))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    video = db.Column(db.String)
    user = db.Column(db.Integer, db.ForeignKey('admin.id'))


@app.route('/')
def home():
    post = Preview.query.all()
    return render_template('home.html', post=post, text='homepage', title='Home')


@app.route('/Super_secret_admin_registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        email = form.email.data
        user = Admin(username=name, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect('/Super_secret_admin_login')
    return render_template('registration.html', form=form, title='Registration')


@app.route('/Super_secret_admin_login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = Admin.query.filter_by(username=username).first()
        if user is None or user.password != password:
            return redirect('/login')
        return redirect('/film_preview_posting')
    return render_template('login.html', title='Super_secret_admin_Login', form=form)


@app.route('/film_preview_posting', methods=['GET', 'POST'])
@login_required
def film_preview_post():
    form = PostForm()
    file = ''
    if request.method == 'POST':
        file = request.files['image']
        file.save(f'app/static/images/{file.filename}')
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        user = Preview(title=title, body=body, image=f'/static/images/{file.filename}')
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('post_create.html', form=form, title='Create')



@app.route("/movie_posting", methods=["POST", "GET"])
def index():
    form = PostForm()
    file = ''
    if request.method == "POST":
        file = request.files["file"]
    if form.validate_on_submit:
        title = form.title.data
        body = form.body.data
        user = Movie(title=title, body=body, video=f'/static/videos/{file.filename}')
        db.session.add(user)
        db.session.commit()
    return render_template("film_post.html",  form=form, title='Create_movie')


@app.route('/del_post/<int:id>')
def post_del(id):
    post = Preview.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')


@app.route('/preview/<int:id>', methods=['POST', 'GET'])
def post(id):
    post = Preview.query.get(id)
    comments = Comment.query.filter_by(post=id)
    form = CommentForm()
    if form.validate_on_submit():
        text = form.text.data
        comment = Comment(body=text, user=current_user.id, post=id)
        db.session.add(comment)
        db.session.commit()
        return redirect(f'/preview/{id}')
    return render_template('preview.html', post=post, form=form, comments=comments)

@app.route('/movie/<int:id>', methods=['POST', 'GET'])
def movie(id):
    post = Movie.query.get(id)
    comments = Comment.query.filter_by(post=id)
    form = CommentForm()
    if form.validate_on_submit():
        text = form.text.data
        comment = Comment(body=text, user=current_user.id, post=id)
        db.session.add(comment)
        db.session.commit()
        return redirect(f'/movie/{id}')
    return render_template('movie.html', post=post, form=form, comments=comments)