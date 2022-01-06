from movie_query import parse_list_input

class CastOriginalityCalculator():
    def __init__(self, query):
        # Handle actors input
        actors_str = input("\nWhich actors would you like to employ? Enter a comma seperated list: ")
        actors = parse_list_input(actors_str)

        if actors is None:
            raise ValueError("Must provide at least one actor")

        result = query.calculate_cast_originality(actors)

        if result is not None:
            print(result)
        else:
            print("No such movies found")