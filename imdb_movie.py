from imdb import IMDb

class IMDBMovie():  
    def __init__(self, search):
        """Setup up variables and initialize with data from IMDb"""
        self.id = None
        self.rating = None

        # create an instance of the IMDb class
        imdb = IMDb()
        try:
            mov = imdb.search_movie(search)[0]
            self.id = mov.getID()

            data = imdb.get_movie_main(mov.getID())['data']

            self.title = data['title']
            try:
                self.rating = data['rating']
            except KeyError:
                pass
        except IndexError:
            # movie not found in IMDb database
            pass
