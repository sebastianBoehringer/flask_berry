from flask import Flask

from app.data.Label import Label


def test_load_label_from_db(app: Flask):
    with app.test_request_context():
        label = Label.from_db(1)
        assert label.id is 1, "Label has different id"
        assert "Test Label" in label.name, "label name [{0}] does not match expected ['Test Label']".format(label.name)


def test_load_non_existent_label_from_db_returns_none(app: Flask):
    with app.test_request_context():
        label = Label.from_db(234)
        assert label is None, "A label with id 234 was found: {0}".format(label)
