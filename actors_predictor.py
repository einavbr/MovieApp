from movie_query import parse_list_input

class ActorsPredictor():
    def __init__(self, query):
        # Handle genres input
        genres_str = input("Which Genres will your movie be? Enter a comma seperated list: ")
        genres = parse_list_input(genres_str)
        
        if genres is None:
            raise ValueError("Must provide at least one genre")

        result = query.predict_actors_by_genre(genres)
        
        if result is not None:
            print(result)
        else:
            print("No such movies found")
