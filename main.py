from movie_query import MovieQuery
from connector import Connector

db_con = Connector()
query = MovieQuery(db_con)

def parse_list_input(str_input):
    lst = str_input.split(",")
    lst = [item.strip().lower() for item in lst]
    return lst

# Handle actors input
actors_str = input("Which actors would you like to employ? Enter a comma seperated list: ")

# Handle genres input
genres_str = input("Which Genres will your movie be? Enter a comma seperated list: ")


# Handle keywords input
keywords = input("Enter Keywords that would be in your movie's overview?")

# Map to correct query
result = ""
if (len(actors_str) > 0 and len(genres_str) > 0 and len(keywords) > 0):
    actors = parse_list_input(actors_str)
    genres = parse_list_input(genres_str)
    # TODO: create predict_by_actors_genres_keywords func
    pass
elif (len(actors_str) > 0 and len(genres_str) > 0):
    actors = parse_list_input(actors_str)
    genres = parse_list_input(genres_str)
    result = query.predict_by_actors_and_genres(actors, genres)
elif (len(actors_str) > 0 and len(keywords) > 0):
    actors = parse_list_input(actors_str)
    # TODO: create predict_by_actors_and_keywords func
    pass
elif (len(genres_str) > 0 and len(keywords) > 0):
    genres = parse_list_input(genres_str)
    # TODO: create predict_by_genres_and_keywords func
    pass
elif (len(actors_str) > 0):
    actors = parse_list_input(actors_str)
    result = query.predict_by_actors(actors)
elif (len(genres_str) > 0):
    genres = parse_list_input(genres_str)
    result = query.predict_by_genres(genres)
elif (len(keywords) > 0):
    result = query.predict_by_keywords(keywords)

if result is not None:
    print(result)
else:
    print("No such movies found")

db_con.close()