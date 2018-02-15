import json

from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


app = CustomFlask(__name__)  # This replaces your existing "app = Flask(__name__)"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.sqlite'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = "TODO: Move the key definition into a config file"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class LoginForm(FlaskForm):
    email = StringField(id="email")
    password = PasswordField(id="password")
    submit = SubmitField(id="submit")


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    average_rating = db.Column(db.Float, default=-1)
    ratings = db.relationship('Rating', backref='movie', lazy=True)

    def __repr__(self):
        return '<Movie %r>' % self.title


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def __init__(self, email=None, password=None):
        if password:
            self.set_password(password)
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        """ This is used by the login_manager's user_loader() function.
        - See https://stackoverflow.com/questions/34951134/flask-login-only-works-if-get-id-returns-self-email

        :return:
        """
        return str(self.id)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)


@app.route("/")
def index():
    form = LoginForm()
    all_movies = get_all_movies_formatted_for_frontend()
    return render_template("index.html", all_movies=all_movies, form=form)


def get_all_movies_formatted_for_frontend():
    all_movies = Movie.query.all()
    all_movies = [{'title': movie.title,
                   'averageRating': movie.average_rating} for movie in all_movies]
    return all_movies


@app.route("/movies/", methods=["POST"])
def add_movie():
    posted_data = json.loads(request.data.decode("utf-8"))
    movie_title = posted_data['movieTitle']

    movie_is_in_db_already = bool(Movie.query.filter(func.lower(Movie.title) == func.lower(movie_title)).first())
    if movie_is_in_db_already:
        message = "The movie is already in the database!"
    else:
        new_movie = Movie(title=movie_title)
        db.session.add(new_movie)
        db.session.commit()

        message = "The movie was added to the database!"

    all_movies = get_all_movies_formatted_for_frontend()

    response_dict = {'message': message, 'movies': all_movies}
    return json.dumps(response_dict)


@app.route('/signin', methods=['POST'])
def signin():
    form = LoginForm()
    response_dict = {}
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            login_user(user)
        else:
            new_user = User(form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
        response_dict['logged_in'] = True
    else:
        response_dict['logged_in'] = False
    return redirect(url_for('index'))


@app.route("/scripts", methods=["POST"])
def upload_script():
    file = request.files['file']
    text_from_the_file = file.read().decode('utf-8')
    predicted_genre = get_predicted_genre_given_text_of_script(text_from_the_file)

    response_dict = {'genre': predicted_genre}
    return json.dumps(response_dict)


@login_required
@app.route("/submit_rating/", methods=["POST"])
def submit_rating():
    posted_data = json.loads(request.data.decode("utf-8"))
    movie_data = posted_data['movie']
    submitted_rating = int(posted_data['rating'])
    assert submitted_rating in range(1, 6)

    selected_movie = Movie.query.filter(func.lower(Movie.title) == func.lower(movie_data['title'])).first()

    existing_user_rating_for_this_movie = Rating.query.filter(Rating.movie_id==selected_movie.id).first()

    if existing_user_rating_for_this_movie:
        rating = existing_user_rating_for_this_movie
        rating.value = submitted_rating
    else:
        rating = Rating(movie_id=selected_movie.id, user_id=current_user.id, value=submitted_rating)
    db.session.add(rating)
    db.session.commit()

    all_ratings = [rating.value for rating in Rating.query.filter(Rating.movie_id==rating.movie_id).all()]
    print(all_ratings)
    average_rating = sum(all_ratings) / len(all_ratings)

    selected_movie.average_rating = average_rating
    db.session.add(selected_movie)
    db.session.commit()

    response_dict = {'averageRating': average_rating}
    return json.dumps(response_dict)


def get_predicted_genre_given_text_of_script(text_of_the_script):
    text_of_the_script = text_of_the_script.replace("\r\n", "\n")
    text_of_the_script = text_of_the_script.strip()
    return text_of_the_script[:10]


if __name__ == "__main__":
    app.run()
