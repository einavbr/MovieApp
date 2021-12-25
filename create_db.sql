CREATE TABLE IF NOT EXISTS imdb_ratings (movie_id INT PRIMARY KEY, rating FLOAT)
;
CREATE TABLE IF NOT EXISTS movies (movie_id INT PRIMARY KEY, title VARCHAR(255) NOT NULL, overview TEXT(5000), release_date DATE, popularity FLOAT, original_language VARCHAR(10), imdb_id INT UNIQUE, FOREIGN KEY(imdb_id) REFERENCES imdb_ratings(movie_id), imdb_name VARCHAR(200))
;
CREATE TABLE IF NOT EXISTS genres (genre_id INT PRIMARY KEY, genre VARCHAR(255))
;
CREATE TABLE IF NOT EXISTS movies_genres (movie_id INT, FOREIGN KEY(movie_id) REFERENCES movies(movie_id), genre_id INT, FOREIGN KEY(genre_id) REFERENCES genres(genre_id))
;
CREATE TABLE IF NOT EXISTS actors (id INT PRIMARY KEY, actor_name VARCHAR(50) NOT NULL, gender VARCHAR(10), popularity FLOAT)
;
CREATE TABLE IF NOT EXISTS movies_actors (movie_id INT, FOREIGN KEY(movie_id) REFERENCES movies(movie_id), actor_id INT, FOREIGN KEY(actor_id) REFERENCES actors(id))
;
-- CREATE VIEW top50_actors AS
-- 	SELECT id, popularity
--     from actors
-- 	order by popularity desc
--     limit 50
-- ;
-- CREATE VIEW top50_movies AS
-- 	SELECT id, popularity
--     from movies
-- 	order by popularity desc
--     limit 50
-- ;
-- SELECT concat('DROP TABLE IF EXISTS `', table_name, '`;')
-- FROM information_schema.tables
-- WHERE table_schema = 'DbMysql15';
-- ;
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `genres`;
DROP TABLE IF EXISTS `movies`;
DROP TABLE IF EXISTS `actors`;
DROP TABLE IF EXISTS `movies_genres`;
DROP TABLE IF EXISTS `movies_actors`;
DROP TABLE IF EXISTS `imdb_ratings`;
DROP TABLE IF EXISTS `purchases`;
SET FOREIGN_KEY_CHECKS = 1;
;
show tables
;

INSERT INTO imdb_ratings (movie_id, rating) VALUES (123456, Null)
;
INSERT INTO imdb_ratings (movie_id) VALUES (123456)
;

select * from movies_genres
;

select * from movies
