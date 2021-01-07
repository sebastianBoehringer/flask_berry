INSERT INTO labels (id, name)
VALUES (1, 'Test Label'),
       (2, 'Test_Case');

INSERT INTO songs(id, name, genre, duration, location)
VALUES (1, 'The great testing', 'experimental', 666, '.');

INSERT INTO song_labels(song_id, label_id)
VALUES (1, 1);

INSERT INTO song_artists(song_id, name)
VALUES (1, 'Patricia Patricide'),
       (1, 'Franco Fratricide');

INSERT INTO song_supporting_artists(song_id, name)
VALUES (1, 'Uma Jan');