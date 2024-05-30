class HelperExtractor:
    @staticmethod
    def count_duplicate_entries(data: list[dict]) -> tuple[dict, dict]:
        """
        Counts the number of entries based on user_id and movie_id.
        :param data: list with dict user id and movie id as key.
        :return:
        """
        grouped_entries = {}
        count_dict = {}
        for entry in data:
            key = (entry['user_id'], entry['movie_id'])
            if key in grouped_entries:
                grouped_entries[key].append(entry)
                count_dict[key] += 1
            else:
                grouped_entries[key] = [entry]
                count_dict[key] = 1
        return grouped_entries, count_dict

    @staticmethod
    def choose_users(user_movie: dict[tuple, str]) -> dict:
        """
        Selects users and their movies, ensuring each user has at most 5 movies.

        :param user_movie: Dictionary with user-movie pairs.
        :return: Dictionary with users as keys and their movies as values.
        """
        unique_first_elements = set()
        users_movie_dict = {}

        for key, value in user_movie.items():
            user_element = key[0]
            movie_element = key[1]

            if user_element not in unique_first_elements:
                unique_first_elements.add(user_element)
                users_movie_dict[user_element] = []

            if len(users_movie_dict[user_element]) < 5:
                users_movie_dict[user_element].append(movie_element)
        return users_movie_dict

    @staticmethod
    def find_last_watched(users_movies: list[dict]) -> dict:
        """
        Finds the last watched movie for each user.
        :param users_movies: List of movies watched by users.
        :return: Dictionary with user IDs as keys and the last watched movie ID as values.
        """
        last_watched_movie = {}
        for movie in users_movies:
            user_id = movie['user_id']
            last_watched_movie[user_id] = [movie['movie_id']]
        return last_watched_movie
