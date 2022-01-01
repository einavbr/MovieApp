# MovieApp
An app that will answer some questions about movies in a custom DB for University project.
Our app will allow script writers to conduct a POC for their movie, provided different information:
- Predicted rating
  * Given a provided list of actors
  * Given a provided list of genres
  * Given a provided list of keywords
  * Given a provided list of actors + genres
  * Given a provided list of actors + keywords
  * Given a provided list of genres + keywords
  * Given a provided list of actors + genres + keywords
- Predicted actors who would want to participate
  * Given a provided list of genres for the movie
- Language best to produce the movie in
  * Provided a list of actors, this shows the most common language the actors use in their movies
- Originality of the cast
  * How many previous movies have been created with a set of actors
- Help the creative juices flow by showing the most popular movies

## Queries
1. Predicted rating - 
2. Predicted income -
3. Predicted budget -
4. Predicted awards -
5. Predicted actors who would want to participate - actors that are the top participants in the movie's genre
6. Language best to produce the movie in - 
7. Locations best to film the movie in - 

## Ways we optimized the code:
- Query for most popular movies
- indexes on actor names and genres
- Use aggregated functions where possible
- Use small varchars where possible

## Other notes:
- Used views for readability and preventing code duplication
