from flask import Flask, render_template

from data import db

app = Flask(__name__)
db.init_app(app)


@app.route('/')
def hello_world():
    return render_template("mainpage")


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=False)
