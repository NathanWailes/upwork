from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")  # render_template() assumes templates will be in a subfolder named 'templates'


if __name__ == "__main__":
    app.run()
