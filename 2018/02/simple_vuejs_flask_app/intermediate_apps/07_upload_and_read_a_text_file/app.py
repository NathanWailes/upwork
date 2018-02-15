import json

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


app = CustomFlask(__name__)  # This replaces your existing "app = Flask(__name__)"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.sqlite'
db = SQLAlchemy(app)

CORS(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Movie %r>' % self.title


@app.route("/")
def index():
    all_movies = Movie.query.all()
    all_movie_titles = [movie.title for movie in all_movies]
    return render_template("index.html", all_movie_titles=all_movie_titles)


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

    response_dict = {'message': message}
    return json.dumps(response_dict)


@app.route("/scripts", methods=["POST"])
def upload_script():
    file = request.files['file']
    text_from_the_file = file.read().decode('utf-8')
    predicted_genre = get_predicted_genre_given_text_of_script(text_from_the_file)

    response_dict = {'genre': predicted_genre}
    return json.dumps(response_dict)


def get_predicted_genre_given_text_of_script(text_of_the_script):
    text_of_the_script = text_of_the_script.replace("\r\n", "\n")
    text_of_the_script = text_of_the_script.strip()
    return text_of_the_script[:10]


if __name__ == "__main__":
    app.run()
