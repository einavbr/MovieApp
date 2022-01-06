from movie_query import parse_list_input

class LanguageCalculator():
    def __init__(self, query):
        # Handle actors input
        actors_str = input("\nWhich actors would you like to employ? Enter a comma seperated list: ")
        actors = parse_list_input(actors_str)

        if actors is None:
            raise ValueError("Must provide at least one actor")

        result = query.find_language_by_actors(actors)
        
        if result is not None:
            print(result)
        else:
            print("No such movies found")
