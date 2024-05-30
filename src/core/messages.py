from dataclasses import dataclass


@dataclass
class Messages:
    rec_added: str
    wrong_type: str
    no_rec_user: str
    no_rec_movie: str
    rec_found_movie: str
    error_find_user: str
    wrong_user_id: str
    error_add_movie: str
    error_select_movie: str
    data_inserted: str
    no_movie_to_rec: str
    error_insert: str
    error_request: str
    no_movie: str
    wrong_movie_type: str
    cache_inserted: str

    def __init__(
        self,
        rec_added: str = 'Recommendations has been added.',
        wrong_type: str = "Wrong recommendation's type. Type: {0}",
        no_rec_user: str = "No one recommendations for user {0}.",
        no_rec_movie: str = "No one recommendation found for movie: {0}",
        rec_found_movie: str = "Recommendations for movie {0} has been found.",
        error_find_user: str = "Error finding cold start users: {0}",
        wrong_user_id: str = "Wrong user id. Error: {0}",
        error_add_movie: str = "Error occurred while adding CS movies: {0}",
        error_select_movie: str = "Error occurred while selecting movies: {0}",
        data_inserted: str = 'Data inserted successfully to {0}',
        no_movie_to_rec: str = "No movies to add recommendations.",
        error_insert: str = 'Error with insert. Info: {0}',
        error_request: str = "Error in request: {0}.",
        no_movie: str = "No one movie",
        wrong_movie_type: str = "Movie must be string. Import is: {0}",
        cache_inserted: str = "Redis inserted. Key: {0}. Value: {1}.",
    ):
        self.rec_added = rec_added
        self.wrong_type = wrong_type
        self.no_rec_user = no_rec_user
        self.no_rec_movie = no_rec_movie
        self.rec_found_movie = rec_found_movie
        self.error_find_user = error_find_user
        self.wrong_user_id = wrong_user_id
        self.error_add_movie = error_add_movie
        self.error_select_movie = error_select_movie
        self.data_inserted = data_inserted
        self.no_movie_to_rec = no_movie_to_rec
        self.error_insert = error_insert
        self.error_request = error_request
        self.no_movie = no_movie
        self.wrong_movie_type = wrong_movie_type
        self.cache_inserted = cache_inserted


message = Messages()
