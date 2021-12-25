

from datetime import datetime
import pymysql

class Connector():
  def __init__(self):

      self.conn = pymysql.connect(
          host='localhost',
          port=3305,
          user='DbMysql15',
          password='DbMysql15',
          database='DbMysql15'
      )
      self.cursor = self.conn.cursor()
  
  def close(self):
      self.cursor.close() 
      self.conn.close()

  def insert_imdb_rating(self, imdb_movie):
    query = 'INSERT INTO imdb_ratings (movie_id, rating) VALUES (%s, %s)'
    null_rating_query = 'INSERT IGNORE INTO imdb_ratings (movie_id) VALUES (%s)'
    
    print(imdb_movie.id)
    movie_id = int(imdb_movie.id)

    if imdb_movie.rating is None:
      self.cursor.execute(null_rating_query, [movie_id])
    else:
      rating = float(imdb_movie.rating)
      data = [
        movie_id,
        rating
      ]
      try:
        self.cursor.execute(query, data)
      except Exception as e:
        # Couldn't insert movie and rating
        self.cursor.execute("select rating from imdb_ratings where movie_id = %s" % movie_id)
        myresult = self.cursor.fetchall()
        if myresult is not None:
          # movie and rating already exist in the database
          pass
        else:
          # movie exists in the database but it's rating is Nan
          print("setting rating")
          set_query = "update imdb_ratings set rating = %s where movie_id = %s"
          self.cursor.execute(set_query, data)
    self.conn.commit()

  def insert_movie_with_imdb_data(self, movie, imdb_movie):
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
    self.cursor.execute(query, data)
    self.conn.commit()

  def insert_movie(self, movie):
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
      self.cursor.execute(query, data)
    except Exception as e:
      print("insert_movie")
      print(e)
      print(data)
    self.conn.commit()

  def insert_genres(self, genre):
    query = 'INSERT INTO genres (genre_id, genre) VALUES (%s, %s)'
    for g in genre.movie_list():
      data = [int(g["id"]), g["name"]]
      self.cursor.execute(query, data)
      self.conn.commit()
    
  def insert_movie_genres(self, movie):
    query = 'INSERT INTO movies_genres (movie_id, genre_id) VALUES (%s, %s)'
    for id in movie.genre_ids:
      data = [
        int(movie.id),
        int(id)
      ]
      self.cursor.execute(query, data)
      self.conn.commit()

  def insert_actors(self, cast):
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
      self.cursor.execute(query, data)
      self.conn.commit()

  def insert_movie_actors(self, movie_id, cast):
    query = 'INSERT INTO movies_actors (movie_id, actor_id) VALUES (%s, %s)'
    for actor in cast:
      data = [
        int(movie_id),
        int(actor.id)
      ]
      self.cursor.execute(query, data)
      self.conn.commit()