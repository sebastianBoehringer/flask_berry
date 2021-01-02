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


def test_can_save_label(app: Flask):
    with app.test_request_context():
        label = Label(name="Test Save")
        label.save()
        assert label.id is not None, "label did not have an id after being saved"
        control_label = Label.from_db(label.id)
        assert control_label is not None, "label with id {0} does not exist".format(label.id)
        assert "Test Save" in control_label.name


def test_can_update_label(app: Flask):
    with app.test_request_context():
        label = Label(name="to change")
        label.save()
        label.name = "Something else"
        label.update()

        control_label = Label.from_db(label.id)
        assert control_label is not None, "could not find a label with the given id {0}".format(label.id)
        assert "Something else" in control_label.name, "label name [{0}] does not match expected ['Something else']". \
            format(label)
