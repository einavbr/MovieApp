from movie_query import parse_list_input

class SimilarityCalculator():
    def __init__(self, query):
        print("\nFor Each Question below, press enter to leave the answer empty.")
        
        # Handle actors input
        actors_str = input("Which actors would you like to employ? Enter a comma seperated list: ")
        actors = parse_list_input(actors_str)

        # Handle genres input
        genres_str = input("Which Genres will your movie be? Enter a comma seperated list: ")
        genres = parse_list_input(genres_str)

        # Handle keywords input
        keywords = input("Enter Keywords that would be in your movie's overview: ")

        result = query.get_similar_movies(actors, genres, keywords)

        if result is not None:
            print(result)
        else:
            print("No such movies found")
