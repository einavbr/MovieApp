from imdb import IMDb

class IMDBMovie():  
    def __init__(self, search):
        """Setup up variables and initialize with data from IMDb"""
        self.id = None
        # self.title = None
        # self.year = None
        # self.runtime = None
        self.rating = None
        # self.summary = None
        # self.actors = {}
        # self.directors = {}
        # self.genres = None

        # create an instance of the IMDb class
        imdb = IMDb()
        try:
            mov = imdb.search_movie(search)[0]
            self.id = mov.getID()

            data = imdb.get_movie_main(mov.getID())['data']

            self.title = data['title']
            # self.year = data['year']
            # self.runtime = int(data['runtimes'][0])
            try:
                self.rating = data['rating']
            except KeyError:
                pass
            # self.summary = data['plot outline']

            # for role, lookup in [('cast', self.actors),
            #                      ('director', self.directors)]:
            #     for person in data[role]:
            #         lookup[person.getID()] = person.data['name']

            # self.genres = data['genres']
        except IndexError:
            # movie not found in IMDb database
            pass
