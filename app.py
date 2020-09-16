from flask import Flask, render_template

app = Flask(__name__)
FLASK_DEBUG = True


@app.route('/')
def hello_world():
    return render_template("mainpage")


if __name__ == '__main__':
    app.run(port="8080", debug=True)
