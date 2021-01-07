import os

import pytest
from flask import Flask

from app.data.Label import Label
from app.data.Song import Song


def test_cannot_save_invalid_song():
    with pytest.raises(Exception):
        # has to have at least one artist
        Song(name="test", main_artists=set(), supporting_artists=set(), location=os.path.curdir, labels=set(),
             duration=1, genre="Test")
        # 0 duration does not make sense
        Song(name="test", main_artists={"test"}, supporting_artists=set(), location=os.path.curdir, labels=set(),
             duration=0, genre="Test")
        # negative duration does not make sense
        Song(name="test", main_artists={"test"}, supporting_artists=set(), location=os.path.curdir, labels=set(),
             duration=-20, genre="Test")


def test_can_load_song_from_database(app: Flask):
    with app.test_request_context():
        control_song = Song(entry_id=1, location=".", duration=666, name="The great testing", genre="experimental",
                            labels={Label.from_db(1)}, main_artists={"Patricia Patricide", "Franco Fratricide"},
                            supporting_artists={"Uma Jan"})
        song = Song.from_db(1)
        assert control_song == song, "Songs aren't equal: expected [{0}], actual [{1}]".format(control_song, song)


def test_can_save_song(app: Flask):
    with app.test_request_context():
        label = Label.from_db(1)
        song = Song(name="test_song", main_artists={"Toni Testosterone"}, supporting_artists={"Sina Support"},
                    duration=104, location=os.path.abspath(__file__), labels={label}, genre="experimental")
        song.save()
        assert song.id is not None, "song is missing id after saving"
        control_song = Song.from_db(song.id)
        assert song == control_song, "Did not load same song from db. saved:[{0}], from db: [{1}]". \
            format(song, control_song)


def test_can_update_song(app: Flask):
    with app.test_request_context():
        song = Song.from_db(1)
        song.name = "The changed ones"
        song.update()
        control_song = Song.from_db(1)
        assert "The changed ones" in control_song.name, "Song names do not match"
        assert song == control_song, "Did not load same song from db. saved:[{0}], from db: [{1}]". \
            format(song, control_song)


def test_can_delete_song(app: Flask):
    with app.test_request_context():
        song = Song(name="temporary song", main_artists={"Toni Testosterone"}, supporting_artists={"Sina Support"},
                    duration=104, location=os.path.abspath(__file__), labels=set(), genre="experimental")
        song.save()
        prior_id = song.id
        assert song.delete()
        assert Song.from_db(prior_id) is None, "Song [{0}] was found, it should have been deleted"


def test_load_non_existent_song_from_db_returns_none(app: Flask):
    with app.test_request_context():
        song = Song.from_db(234)
        assert song is None, "A song with id 234 was found: {0}".format(song)
