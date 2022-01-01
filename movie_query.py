from connector import Connector

def parse_list_input(str_input):
    if len(str_input) == 0:
        return None
    lst = str_input.split(",")
    lst = [item.strip().lower() for item in lst]
    return lst

class MovieQuery():
    def __init__(self, db_con:Connector):
        self.db_con = db_con

    ###  ------------------------- Private methods -------------------------------- ###

    def __format_rating_response(self, response):
        try:
            return round(float(response[0][0]), 2)
        except IndexError:
            return None
    
    def __format_language_response(self, response):
        try:
            return (response[0][0])
        except IndexError:
            return None

    def __alter_movie_ids_view_by_actors(self, actors):
        where = self.__create_where_clause(actors, "actor_name")
        # Get a list of all movies with all these actors
        get_movie_ids_query = "CREATE OR REPLACE VIEW actor_movie_ids AS \
            SELECT ma.movie_id \
            FROM actors as a \
            JOIN movies_actors as ma \
            ON a.id = ma.actor_id \
            WHERE " + where + \
            "GROUP BY ma.movie_id \
            HAVING count(distinct ma.actor_id) >= %s"
        self.execute_query(get_movie_ids_query, [len(actors)])
    
    def __alter_movie_ids_view_by_genres(self, genres):
        where = self.__create_where_clause(genres, "genre")
        # Get a list of all movies with all these genres
        get_movie_ids_query = "CREATE OR REPLACE VIEW genre_movie_ids AS \
            SELECT mg.movie_id \
            FROM genres as g \
            JOIN movies_genres as mg \
            ON g.genre_id = mg.genre_id \
            WHERE " + where + \
            " GROUP BY mg.movie_id \
            HAVING count(distinct mg.genre_id) >= %s"
        self.execute_query(get_movie_ids_query, [len(genres)])
    
    def __create_where_clause(self, lst, col_name:str):
        if lst is not None:
            col_name = "lower(" + col_name + ")"
            where = col_name + " like '" + lst[0] + "'"
            for i in range(1, len(lst)):
                where = where + " or " + col_name + " like '" + lst[i] + "'"
            return where
        else:
            return "true"
    
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
            return self.__format_rating_response(self.db_con.cursor.fetchall())
        except TypeError:
            print("No movies with this combination")
            return None
    
    def __create_keywords_query(self, keywords, where_clause = ""):
        return f"""
            select distinct sum(rating * (match_score/ sum_scores)) over() as weighted_avg_rating
            from (
                select t.movie_id,
                    rating,
                    match_score,
                    sum(match_score) over () as sum_scores
                from (
                    select m.movie_id,
                        overview,
                        rating,
                        match(overview) against ("{keywords}") as match_score
                    from movies as m
                    left join imdb_ratings as ir
                    on m.imdb_id = ir.movie_id
                    {where_clause}
                    having match_score > 0
                ) as t
            )as t2
        """

    ###  ------------------------- Public methods -------------------------------- ###

    def execute_query(self, query, args = None):
        self.db_con.cursor.execute(query, args)
        self.db_con.conn.commit()

    def rating_per_actor(self, actors):
        for actor in actors:
            query = "SELECT popularity FROM actors WHERE lower(actor_name) like %s"
            self.db_con.cursor.execute(query, [actor])
            this_result = self.db_con.cursor.fetchall()
            return self.__format_rating_response(this_result)

    def predict_rating_by_actors(self, actors):
        self.__alter_movie_ids_view_by_actors(actors)
        # Get the average imdb rating for movies with these actors
        rating = self.__get_avg_rating("actor_movie_ids")
        return rating

    def predict_rating_by_genres(self, genres):
        self.__alter_movie_ids_view_by_genres(genres)
        # Get the average imdb rating for movies with these genres
        rating = self.__get_avg_rating("genre_movie_ids")
        return rating
    
    def predict_rating_by_actors_and_genres(self, actors, genres):
        self.__alter_movie_ids_view_by_actors(actors)
        self.__alter_movie_ids_view_by_genres(genres)
        query = """CREATE OR REPLACE VIEW movie_ids AS
            SELECT g.movie_id
            FROM genre_movie_ids as g
            JOIN actor_movie_ids as a
            ON g.movie_id = a.movie_id"""
        self.execute_query(query)

        rating = self.__get_avg_rating("movie_ids")
        return rating
    
    def predict_rating_by_keywords(self, keywords):
        query = self.__create_keywords_query(keywords)
        self.execute_query(query)
        return self.__format_rating_response(self.db_con.cursor.fetchall())

    def predict_rating_by_actors_genres_keywords(self, actors, genres, keywords):
        self.__alter_movie_ids_view_by_actors(actors)
        self.__alter_movie_ids_view_by_genres(genres)
        where_clause = """
            where m.movie_id in (
                select g.movie_id
                from genre_movie_ids as g
                join actor_movie_ids as a
                on g.movie_id = a.movie_id
            )
        """
        query = self.__create_keywords_query(keywords, where_clause)
        self.execute_query(query)
        return self.__format_rating_response(self.db_con.cursor.fetchall())

    def predict_rating_by_actors_and_keywords (self, actors, keywords):
        self.__alter_movie_ids_view_by_actors(actors)
        where_clause = """
            where m.movie_id in (
                select movie_id
                from actor_movie_ids
            )
        """
        query = self.__create_keywords_query(keywords, where_clause)
        self.execute_query(query)
        return self.__format_rating_response(self.db_con.cursor.fetchall())

    def predict_rating_by_genres_and_keywords (self, genres, keywords):
        self.__alter_movie_ids_view_by_genres(genres)
        where_clause = """
            where m.movie_id in (
                select movie_id
                from genre_movie_ids
            )
        """
        query = self.__create_keywords_query(keywords, where_clause)
        self.execute_query(query)
        return self.__format_rating_response(self.db_con.cursor.fetchall())
    
    def predict_actors_by_genre(self, genres):
        where = self.__create_where_clause(genres, "genre")
        query = f"""
            select distinct a.actor_name,
                a.popularity
            from genres as g
            join movies_genres as mg
            on g.genre_id = mg.genre_id
            join movies as m
            on m.movie_id = mg.movie_id
            join movies_actors as ma
            on ma.movie_id = m.movie_id
            join actors as a
            on a.id = ma.actor_id
            where {where}
            order by a.popularity desc
            limit 20
        """
        self.execute_query(query)
        return self.db_con.cursor.fetchall()
    
    def get_similar_movies(self, actors, genres, keywords):
        actors_where_clause = self.__create_where_clause(actors, "actor_name")
        genres_where_clause = self.__create_where_clause(genres, "genre")
        query = f"""CREATE OR REPLACE VIEW similar_movies AS 
            select m.movie_id,
                m.title,
                count(distinct a.id) as amount_relevant_actors,
                count(distinct g.genre_id) as amount_relevant_genres,
                match(overview) against ("{keywords}") as overview_match_score
            from genres as g
            join movies_genres as mg
            on g.genre_id = mg.genre_id
            join movies as m
            on m.movie_id = mg.movie_id
            join movies_actors as ma
            on ma.movie_id = m.movie_id
            join actors as a
            on a.id = ma.actor_id
            where ({actors_where_clause})
                and
                ({genres_where_clause})
            group by m.movie_id, m.title
            limit 50
        """
        self.execute_query(query)

        # actors and genres each provide 50% of the base score, which is then multiplied by the overview_match_score
        amount_actors = len(actors) if actors is not None else "amount_relevant_actors"
        amount_genres = len(genres) if genres is not None else "amount_relevant_genres"
        overview_match_score = "overview_match_score" if len(keywords) > 0 else 1
        similarity_percentage_query = f"""
            select title,
                round(((amount_relevant_actors / {amount_actors} * 50) + (amount_relevant_genres / {amount_genres} * 50)) * {overview_match_score}, 2) as similarity_rating
            from similar_movies
            order by similarity_rating desc
        """
        self.execute_query(similarity_percentage_query)
        return self.db_con.cursor.fetchall()
    
    def find_language_by_actors(self, actors):
        # INTERSECT is not supported for MySQL, therefor using IN
        where_clause = ""
        for i in range(len(actors)):
            if i > 0:
                where_clause += " and "
            where_clause += f"""
            original_language in (
                select original_language
                from actors as a
                join movies_actors as ma
                on ma.actor_id = a.id
                join movies as m
                on m.movie_id = ma.movie_id
                where lower(a.actor_name) = "{actors[i]}"
            )
            """
        query = f"""
            select distinct original_language
            from movies 
            where {where_clause}
        """
        self.execute_query(query)
        return self.__format_language_response(self.db_con.cursor.fetchall())
    
    def calculate_cast_originality(self, actors):
        where_clause = self.__create_where_clause(actors, "actor_name")
        query = f"""
            select count(*) as amount_movies
            from (
                select m.movie_id,
                    count(distinct a.id) as amount_actors_in_movie
                from actors as a
                join movies_actors as ma
                on ma.actor_id = a.id
                join movies as m
                on m.movie_id = ma.movie_id
                where {where_clause}
                group by m.movie_id
            ) as t
            where amount_actors_in_movie = {len(actors)}
        """
        self.execute_query(query)
        return self.__format_rating_response(self.db_con.cursor.fetchall())