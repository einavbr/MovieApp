from movie_query import parse_list_input

class RatingPredictor():
    def __init__(self, query):
        print("For Each Question below, press enter to leave the answer empty.\n")
        # Handle actors input
        actors_str = input("Which actors would you like to employ? Enter a comma seperated list: ")

        # Handle genres input
        genres_str = input("Which Genres will your movie be? Enter a comma seperated list: ")

        # Handle keywords input
        keywords = input("Enter Keywords that would be in your movie's overview: ")

        # Map to correct query
        result = ""
        if (len(actors_str) > 0 and len(genres_str) > 0 and len(keywords) > 0):
            actors = parse_list_input(actors_str)
            genres = parse_list_input(genres_str)
            result = query.predict_rating_by_actors_genres_keywords(actors, genres, keywords)
        elif (len(actors_str) > 0 and len(genres_str) > 0):
            actors = parse_list_input(actors_str)
            genres = parse_list_input(genres_str)
            result = query.predict_rating_by_actors_and_genres(actors, genres)
        elif (len(actors_str) > 0 and len(keywords) > 0):
            actors = parse_list_input(actors_str)
            result = query.predict_rating_by_actors_and_keywords(actors, keywords)
        elif (len(genres_str) > 0 and len(keywords) > 0):
            genres = parse_list_input(genres_str)
            result = query.predict_rating_by_genres_and_keywords(genres, keywords)
        elif (len(actors_str) > 0):
            actors = parse_list_input(actors_str)
            result = query.predict_rating_by_actors(actors)
        elif (len(genres_str) > 0):
            genres = parse_list_input(genres_str)
            result = query.predict_rating_by_genres(genres)
        elif (len(keywords) > 0):
            result = query.predict_rating_by_keywords(keywords)

        if result is not None:
            print(result)
        else:
            print("No such movies found")
