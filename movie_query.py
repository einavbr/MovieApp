from connector import Connector

class MovieQuery():
    def __init__(self, db_con:Connector):
        self.db_con = db_con

    ###  ------------------------- Private methods -------------------------------- ###
    def __alter_movie_ids_view(self, query, args = None):
        self.db_con.cursor.execute(query, args)
        self.db_con.conn.commit()
    
    def __alter_movie_ids_view_by_actors(self, actors):
        where = self.__create_where_clause(actors, "actor_name")
        # Get a list of all movies with all these actors
        get_movie_ids_query = "ALTER VIEW actor_movie_ids AS \
            SELECT ma.movie_id \
            FROM actors as a \
            JOIN movies_actors as ma \
            ON a.id = ma.actor_id \
            WHERE " + where + \
            "GROUP BY ma.movie_id \
            HAVING count(distinct ma.actor_id) >= %s"
        self.__alter_movie_ids_view(get_movie_ids_query, [len(actors)])
    
    def __alter_movie_ids_view_by_genres(self, genres):
        where = self.__create_where_clause(genres, "genre")
        # Get a list of all movies with all these genres
        get_movie_ids_query = "ALTER VIEW genre_movie_ids AS \
            SELECT mg.movie_id \
            FROM genres as g \
            JOIN movies_genres as mg \
            ON g.genre_id = mg.genre_id \
            WHERE " + where + \
            " GROUP BY mg.movie_id \
            HAVING count(distinct mg.genre_id) >= %s"
        self.__alter_movie_ids_view(get_movie_ids_query, [len(genres)])
    
    def __get_movie_ids_view_results(self, view_name):
        self.db_con.cursor.execute("SELECT * FROM %s" % view_name)
        return self.db_con.cursor.fetchall()
    
    def __create_where_clause(self, list, col_name:str):
        col_name = "lower(" + col_name + ")"
        where = col_name + " like '" + list[0] + "'"
        for i in range(1, len(list)):
           where = where + " or " + col_name + " like '" + list[i] + "'"
        return where
    
    def __get_avg_rating(self, view_name):
        # Get the average imdb rating for movies with these genres
        get_avg_rating_query = "SELECT avg(rating) as rating \
            FROM imdb_ratings as ir \
            JOIN movies as m \
            ON ir.movie_id = m.imdb_id \
            WHERE m.movie_id in ( \
                SELECT * \
                FROM " + view_name + \
            " )"
        self.db_con.cursor.execute(get_avg_rating_query)
        try:
            avg_rating = round(float(self.db_con.cursor.fetchall()[0][0]), 2)
            print(avg_rating)
            return avg_rating
        except TypeError:
            print("No movies with this combination")
            return None

    ###  ------------------------- Public methods -------------------------------- ###

    def rating_per_actor(self, actors):
        for actor in actors:
            query = "SELECT popularity FROM actors WHERE lower(actor_name) like %s"
            self.db_con.cursor.execute(query, [actor])
            this_result = self.db_con.cursor.fetchall()
            try:
                rating = round(float(this_result[0][0]), 2)
                print(rating)
                return rating
            except IndexError:
                print("%s not found" % actor)
                return None

    def predict_by_actors(self, actors):
        self.__alter_movie_ids_view_by_actors(actors)
        # Get the average imdb rating for movies with these actors
        rating = self.__get_avg_rating("actor_movie_ids")
        return rating

    def predict_by_genres(self, genres):
        self.__alter_movie_ids_view_by_genres(genres)
        # Get the average imdb rating for movies with these genres
        rating = self.__get_avg_rating("genre_movie_ids")
        return rating
    
    def predict_by_actors_and_genres(self, actors, genres):
        self.__alter_movie_ids_view_by_actors(actors)
        self.__alter_movie_ids_view_by_genres(genres)
        query = """ALTER VIEW movie_ids AS
            SELECT g.movie_id
            FROM genre_movie_ids as g
            JOIN actor_movie_ids as a
            ON g.movie_id = a.movie_id"""
        self.__alter_movie_ids_view(query)

        rating = self.__get_avg_rating("movie_ids")
        print(rating)
        return rating
