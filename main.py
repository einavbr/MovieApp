from tmdbv3api import TMDb, Genre, Movie
from table_create_utils import insert_imdb_rating, insert_movie_with_imdb_data, insert_movie, insert_genres, insert_movie_genres, insert_actors, insert_movie_actors
from imdb_movie import IMDBMovie

TABLE_PATH_PREFIX = '/Users/einavb/tauProjects/DBServices/'

# create an instance of the TMDb class
tmdb = TMDb()
tmdb.api_key = "6c5d2522091c508a9bca48690c7fdf13"
# create instances of TMDb objects
movie = Movie()
genre = Genre()

insert_genres(genre)

for i in range(1,120):
    print(i)
    popular = movie.popular(i)
    for p in popular:
        imdb_movie = IMDBMovie(p.title)
        try:
            insert_imdb_rating(imdb_movie)
            insert_movie_with_imdb_data(p, imdb_movie)
        except Exception:
            # movie doesn't exist in IMDb database or wrong match to imdbId
            print("Movie not found")
            insert_movie(p)
        insert_movie_genres(p)
        response = movie.credits(p.id)
        insert_actors(response['cast'])
        insert_movie_actors(p.id, response['cast'])