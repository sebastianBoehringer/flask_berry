Drop table if exists albums;
Drop table if exists album_labels;
Drop Table if exists album_songs;
Drop table if exists books;
DROP table if exists book_labels;
Drop table if exists book_authors;
Drop table if exists labels;
Drop table if exists timestamps;
Drop table if exists songs;
Drop table if exists song_artists;
DROP table if exists song_supporting_artists;
DROP table if exists song_labels;

Create table labels
(
    id   INTEGER primary key,
    name varchar UNIQUE NOT NULL
);

Create table books
(
    id        INTEGER primary key,
    publisher varchar NOT NULL,
    name      varchar Not NULL,
    location  varchar Not NULL UNIQUE
);

create table book_labels
(
    book_id  INTEGER NOT NULL,
    label_id INTEGER NOT NULL,
    PRIMARY KEY (book_id, label_id),
    FOREIGN KEY (book_id) REFERENCES albums (id),
    FOREIGN KEY (label_id) REFERENCES labels (id)
);

Create table book_authors
(
    author  varchar NOT NULL,
    book_id INTEGER NOt null,
    primary key (author, book_id)
);

Create table albums
(
    id       INTEGER PRIMARY KEY,
    name     varchar        NOT NULL,
    location varchar unique Not NULL,
    artist   varchar        Not NULL,
    CONSTRAINT unique_album_name_artist_combo UNIQUE (name, artist)
);

CREATE table album_labels
(
    album_id INTEGER NOT NULL,
    label_id INTEGER NOT NULL,
    PRIMARY KEY (album_id, label_id),
    FOREIGN KEY (album_id) REFERENCES albums (id),
    FOREIGN KEY (label_id) REFERENCES labels (id)
);

CREATE table album_songs
(
    album_id INTEGER NOT NULL,
    song_id  INTEGER NOT NULL,
    PRIMARY KEY (album_id, song_id),
    FOREIGN KEY (album_id) references albums (id),
    FOREIGN KEY (song_id) references songs (id)
);

CREATE table timestamps
(
    album_id INTEGER NOT NULL,
    song_id  INTEGER NOT NULL,
    start    integer NOT NULL,
    end      integer NOT NULL,
    primary key (album_id, start, end),
    FOREIGN KEY (album_id) references albums (id),
    FOREIGN KEY (song_id) references songs (id),
    CONSTRAINT timestamp_positive_start CHECK (start > 0),
    CONSTRAINT timestamp_positive_end CHECK (end > 0)
);

Create table songs
(
    id       INTEGER PRIMARY KEY,
    name     varchar       NOT NULL,
    genre    varchar,
    duration int           NOT NULL,
    location varchar unique not null,
    CONSTRAINT positive_song_duration CHECK (duration > 0)
);

CREATE table song_supporting_artists
(
    song_id INTEGER NOT NULL,
    name    varchar NOT NULL,
    PRIMARY KEY (song_id, name),
    FOREIGN KEY (song_id) REFERENCES songs (id)
);

CREATE table song_artists
(
    song_id INTEGER NOT NULL,
    name    varchar NOT NULL,
    PRIMARY KEY (song_id, name),
    FOREIGN KEY (song_id) REFERENCES songs (id)
);

CREATE table song_labels
(
    song_id  INTEGER NOT NULL,
    label_id INTEGER NOT NULL,
    PRIMARY KEY (song_id, label_id),
    FOREIGN KEY (song_id) REFERENCES albums (id),
    FOREIGN KEY (label_id) REFERENCES labels (id)
);
