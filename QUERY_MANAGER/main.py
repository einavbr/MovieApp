from rating_predictor import RatingPredictor
from actors_predictor import ActorsPredictor
from similarity_calculator import SimilarityCalculator
from language_calculator import LanguageCalculator
from cast_originality_calculator import CastOriginalityCalculator
from movie_query import MovieQuery
import pymysql

CONNECTOR = pymysql.connect(
    host='localhost',
    port=3305,
    user='DbMysql15',
    password='DbMysql15',
    database='DbMysql15'
)

query = MovieQuery(CONNECTOR)

what_to_predict = """
Welcome to POsCript! The best app in the world for your movie POCs.

What would you like to predict today?
1 - I have an idea for a movie and I want to predict it's rating
2 - I want to know which actors would want to participate in my movie
3 - I have an idea for a movie and I want to know which similar movies have been created
4 - I want to know which languages I can make my movie in
5 - I want to know if my cast is original
6 - HELP! I don't have an idea. Show me the most popular movies in your DB

"""

navigate = input(what_to_predict)

if navigate == '1': 
    RatingPredictor(query)
elif navigate == '2': 
    ActorsPredictor(query)
elif navigate == '3':
    SimilarityCalculator(query)
elif navigate == '4':
    LanguageCalculator(query)
elif navigate == '5':
    CastOriginalityCalculator(query)
elif navigate == '6':
    query_pop_view = "select * from top50_movies"
    query.execute_query(query_pop_view)
    print(CONNECTOR.cursor.fetchall())

CONNECTOR.close()
