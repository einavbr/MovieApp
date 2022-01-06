CREATE TABLE IF NOT EXISTS imdb_ratings (movie_id INT PRIMARY KEY, rating FLOAT);
CREATE TABLE IF NOT EXISTS movies (
    movie_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    overview TEXT(5000),
    release_date DATE,
    popularity FLOAT,
    original_language VARCHAR(10),
    imdb_id INT UNIQUE,
    FOREIGN KEY(imdb_id) REFERENCES imdb_ratings(movie_id),
    imdb_name VARCHAR(200)
);
CREATE TABLE IF NOT EXISTS genres (genre_id INT PRIMARY KEY, genre VARCHAR(255));
CREATE TABLE IF NOT EXISTS movies_genres (
    movie_id INT,
    FOREIGN KEY(movie_id) REFERENCES movies(movie_id),
    genre_id INT,
    FOREIGN KEY(genre_id) REFERENCES genres(genre_id)
);
CREATE TABLE IF NOT EXISTS actors (
    id INT PRIMARY KEY,
    actor_name VARCHAR(50) NOT NULL,
    gender VARCHAR(10),
    popularity FLOAT
);
CREATE TABLE IF NOT EXISTS movies_actors (
    movie_id INT,
    FOREIGN KEY(movie_id) REFERENCES movies(movie_id),
    actor_id INT,
    FOREIGN KEY(actor_id) REFERENCES actors(id)
);
CREATE FULLTEXT INDEX overview_index ON movies(overview);
CREATE INDEX actors_index ON actors (actor_name);
CREATE INDEX genres_index ON genres (genre);
CREATE VIEW top50_movies AS
SELECT title
from movies
order by popularity desc
limit 50;
CREATE VIEW amount_movies_in_db AS
SELECT count(distinct movie_id) as amount_movies
from movies