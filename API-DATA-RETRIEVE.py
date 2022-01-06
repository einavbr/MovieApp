from datetime import datetime
import pymysql
from tmdbv3api import TMDb, Genre, Movie
from imdb_movie import IMDBMovie

TABLE_PATH_PREFIX = '/Users/einavb/tauProjects/DBServices/'
CONNECTOR = pymysql.connect(
    host='localhost',
    port=3305,
    user='DbMysql15',
    password='DbMysql15',
    database='DbMysql15'
)
CURSOR = CONNECTOR.cursor()

# create an instance of the TMDb class
tmdb = TMDb()
tmdb.api_key = "6c5d2522091c508a9bca48690c7fdf13"

# create instances of TMDb objects
movie = Movie()
genre = Genre()

def close_connection():
    CURSOR.close() 
    CONNECTOR.close()

def insert_imdb_rating(imdb_movie):
    query = 'INSERT INTO imdb_ratings (movie_id, rating) VALUES (%s, %s)'
    null_rating_query = 'INSERT IGNORE INTO imdb_ratings (movie_id) VALUES (%s)'

    print(imdb_movie.id)
    movie_id = int(imdb_movie.id)

    if imdb_movie.rating is None:
        CURSOR.execute(null_rating_query, [movie_id])
    else:
        rating = float(imdb_movie.rating)
        data = [
        movie_id,
        rating
        ]
        try:
            CURSOR.execute(query, data)
        except Exception as e:
            # Couldn't insert movie and rating
            CURSOR.execute("select rating from imdb_ratings where movie_id = %s" % movie_id)
            myresult = CURSOR.fetchall()
        if myresult is not None:
            # movie and rating already exist in the database
            pass
        else:
            # movie exists in the database but it's rating is Nan
            print("setting rating")
            set_query = "update imdb_ratings set rating = %s where movie_id = %s"
            CURSOR.execute(set_query, data)
    CONNECTOR.commit()

def insert_movie_with_imdb_data(movie, imdb_movie):
    query = 'INSERT INTO movies (movie_id, title, overview, release_date, popularity, original_language, imdb_id, imdb_name) ' \
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    release_date = ""
    try:
        release_date = datetime.strptime(movie.release_date, '%Y-%m-%d')
    except (AttributeError, ValueError):
        release_date = None

    data = [
        int(movie.id),
        movie.title, 
        movie.overview, 
        release_date,
        float(movie.popularity),
        movie.original_language,
        int(imdb_movie.id),
        imdb_movie.title
    ]
    CURSOR.execute(query, data)
    CONNECTOR.commit()

def insert_movie(movie):
    query = 'INSERT INTO movies (movie_id, title, overview, release_date, popularity, original_language) ' \
        'VALUES (%s, %s, %s, %s, %s, %s)'
    release_date = ""
    try:
        release_date = datetime.strptime(movie.release_date, '%Y-%m-%d')
    except (AttributeError, ValueError):
        release_date = None

    data = [
        int(movie.id),
        movie.title, 
        movie.overview, 
        release_date,
        float(movie.popularity),
        movie.original_language
    ]
    try:
        CURSOR.execute(query, data)
    except Exception as e:
        print("insert_movie")
        print(e)
        print(data)
    CONNECTOR.commit()

def insert_genres(genre):
    query = 'INSERT INTO genres (genre_id, genre) VALUES (%s, %s)'
    for g in genre.movie_list():
        data = [int(g["id"]), g["name"]]
        CURSOR.execute(query, data)
        CONNECTOR.commit()

def insert_movie_genres(movie):
    query = 'INSERT INTO movies_genres (movie_id, genre_id) VALUES (%s, %s)'
    for id in movie.genre_ids:
        data = [
        int(movie.id),
        int(id)
        ]
        CURSOR.execute(query, data)
        CONNECTOR.commit()

def insert_actors(cast):
    query = 'INSERT IGNORE INTO actors (id, actor_name, gender, popularity) ' \
        'VALUES (%s, %s, %s, %s)'
    for actor in cast:
        gender = ''
        if actor['gender'] == '1':
            gender = 'Female'
        if actor['gender'] == '2':
            gender = 'Male'
        else:
            gender = 'Unknown'

        data = [
        int(actor['id']),
        actor['name'],
        gender,
        float(actor['popularity'])
        ]
        CURSOR.execute(query, data)
        CONNECTOR.commit()

def insert_movie_actors(movie_id, cast):
    query = 'INSERT INTO movies_actors (movie_id, actor_id) VALUES (%s, %s)'
    for actor in cast:
        data = [
        int(movie_id),
        int(actor.id)
        ]
        CURSOR.execute(query, data)
        CONNECTOR.commit()


### MAIN ###
insert_genres(genre)

for i in range(1,120):
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

close_connection()