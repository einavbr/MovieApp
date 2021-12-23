

from datetime import datetime
from mysql import connector
from pymysql import err

conn = connector.connect(
    host='localhost',
    port=3305,
    user='DbMysql15',
    password='DbMysql15',
    database='DbMysql15'
)
my_cursor = conn.cursor()

def insert_imdb_rating(imdb_movie):
  query = 'INSERT INTO imdb_ratings (movie_id, rating) VALUES (%s, %s)'
  null_rating_query = 'INSERT IGNORE INTO imdb_ratings (movie_id) VALUES (%s)'
  
  print(imdb_movie.id)
  movie_id = int(imdb_movie.id)

  if imdb_movie.rating is None:
    my_cursor.execute(null_rating_query, [movie_id])
  else:
    rating = float(imdb_movie.rating)
    data = [
      movie_id,
      rating
    ]
    try:
      my_cursor.execute(query, data)
    except Exception as e:
      # Couldn't insert movie and rating
      my_cursor.execute("select rating from imdb_ratings where movie_id = %s" % movie_id)
      myresult = my_cursor.fetchall()
      if myresult is not None:
        # movie and rating already exist in the database
        pass
      else:
        # movie exists in the database but it's rating is Nan
        print("setting rating")
        set_query = "update imdb_ratings set rating = %s where movie_id = %s"
        my_cursor.execute(set_query, data)
  conn.commit()

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
  my_cursor.execute(query, data)
  conn.commit()

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
    my_cursor.execute(query, data)
  except Exception as e:
    print("insert_movie")
    print(e)
    print(data)
  conn.commit()

def insert_genres(genre):
  query = 'INSERT INTO genres (genre_id, genre) VALUES (%s, %s)'
  for g in genre.movie_list():
    data = [int(g["id"]), g["name"]]
    my_cursor.execute(query, data)
    conn.commit()
  
def insert_movie_genres(movie):
  query = 'INSERT INTO movies_genres (movie_id, genre_id) VALUES (%s, %s)'
  for id in movie.genre_ids:
    data = [
      int(movie.id),
      int(id)
    ]
    my_cursor.execute(query, data)
    conn.commit()

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
    my_cursor.execute(query, data)
    conn.commit()

def insert_movie_actors(movie_id, cast):
  query = 'INSERT INTO movies_actors (movie_id, actor_id) VALUES (%s, %s)'
  for actor in cast:
    data = [
      int(movie_id),
      int(actor.id)
    ]
    my_cursor.execute(query, data)
    conn.commit()