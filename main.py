from movie_query import MovieQuery
from connector import Connector

db_con = Connector()
query = MovieQuery(db_con)

def parse_list_input(str_input):
    lst = str_input.split(",")
    lst = [item.strip().lower() for item in lst]
    return lst

# actors_str = input("Which actors would you like to employ? Enter a comma seperated list: ")
# actors = actors_str.split(",")
# actors = [name.strip().lower() for name in actors]

genres_str = input("Which Genres will your movie be? Enter a comma seperated list: ")
genres = parse_list_input(genres_str)

actors_str = input("Which actors would you like to employ? Enter a comma seperated list: ")
actors = parse_list_input(actors_str)

# query.predict_by_actors(actors)
query.predict_by_actors_and_genres(actors, genres)

db_con.close()