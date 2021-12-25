from tmdbv3api import TMDb, Genre, Movie
from connector import Connector
from imdb_movie import IMDBMovie

TABLE_PATH_PREFIX = '/Users/einavb/tauProjects/DBServices/'

# create instance of DB Connector
db_con = Connector()
# create an instance of the TMDb class
tmdb = TMDb()
tmdb.api_key = "6c5d2522091c508a9bca48690c7fdf13"
# create instances of TMDb objects
movie = Movie()
genre = Genre()

db_con.insert_genres(genre)

for i in range(1,120):
    popular = movie.popular(i)
    for p in popular:
        imdb_movie = IMDBMovie(p.title)
        try:
            db_con.insert_imdb_rating(imdb_movie)
            db_con.insert_movie_with_imdb_data(p, imdb_movie)
        except Exception:
            # movie doesn't exist in IMDb database or wrong match to imdbId
            print("Movie not found")
            db_con.insert_movie(p)
        db_con.insert_movie_genres(p)
        response = movie.credits(p.id)
        db_con.insert_actors(response['cast'])
        db_con.insert_movie_actors(p.id, response['cast'])

db_con.close()