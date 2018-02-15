import sqlite3
import predictor

from flask import Flask, render_template, request, jsonify
app = Flask(__name__,
            static_folder = "./static",
            template_folder = "./templates")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    scr = request.get_json()
    preds = predictor.run(scr)
    return jsonify(preds)

@app.route('/title/', methods=['GET'])
def insert_title():
    """
    Connect to database and insert new title
    """
    con = sqlite3.connect('data.db')
    c = con.cursor()
    tilte = str(request.get_json())
    c.execute("""INSERT OR IGNORE
                 INTO ratings
                 VALUES (?,?);""", (title, None))
    con.commit()
    con.close()

@app.route('/vote/', methods=['GET', 'POST'])
def update_rating():
    """
    Update rating for specified title
    """
    con = sqlite3.connect('data.db')
    c = con.cursor()
    title, rating = list(request.get_json()).split()
    c.execute("SELECT Rating FROM ratings WHERE Title=?", (title,))

    # Find new rating
    old_rating = c.fetchone()[-1]
    if old_rating == None:
        new_rating = rating
    else:
        new_rating = round((new_rating + old_rating) / 2, 2)

    # Update entry with new rating
    c.execute("UPDATE ratings SET Rating=? WHERE Title=?", (new_rating,title))
    con.commit()

    # Return the full table
    c.execute("SELECT * FROM raings")
    res = c.fetchall()
    con.close()
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=port)
