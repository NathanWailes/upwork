import json

from flask import Flask, render_template, request


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


app = CustomFlask(__name__)  # This replaces your existing "app = Flask(__name__)"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/movies/", methods=["POST"])
def add_movie():
    posted_data = json.loads(request.data.decode("utf-8"))
    movie_title = posted_data['movieTitle']

    response_dict = { 'message': "Hello from the server! The data was POSTed successfully! You POSTed the movie %s!" % movie_title }
    return json.dumps(response_dict)


if __name__ == "__main__":
    app.run()
