import os

from app.data.Book import Book
from flask import Flask, render_template, jsonify, request

from app.data import db
from app.data.Label import Label


def create_app(test_config=None) -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flask_berry.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello_world():
        return render_template("mainpage")

    @app.route('/books', methods=['POST'])
    def create_book():

        req_data = request.get_json()
        book = Book(name=req_data['name'], location=req_data['location'], entry_id=getattr(req_data, 'id', None),
                    publisher=req_data['publisher'],
                    labels={Label(name=label['name'], label_id=getattr(label, 'id', None)) for label in
                            req_data['labels']}, authors={author for author in req_data['authors']})
        book.save()
        return jsonify(book.as_dict())

    @app.route('/books/<int:id>', methods=['GET'])
    def get_book(id: int):
        book = Book.from_db(id)
        return jsonify(book.as_dict())

    db.init_app(app)
    return app
