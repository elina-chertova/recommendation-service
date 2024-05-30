import io
import pickle
import tempfile
from typing import Any

import pandas as pd
from scipy import sparse

from src.core.logger import logger
from src.core.messages import message
from src.rec_sys.base import RecSystem
from src.utils.cloud import Dropbox


class ItemBased(RecSystem):
    def __init__(self):
        self.model_name: str = "/knn_item_based"
        self.recommend_number: int = 10
        self.cloud = Dropbox()
        self.movies = pd.read_csv(io.BytesIO(self.cloud.download('/movies.csv')))
        self.preferences = pd.read_csv(io.BytesIO(self.cloud.download('/preferences.csv')))
        self.matrix_name = '/movies_matrix.npz'
        self.csr_matrix = self._load_matrix()
        self.model = self._load_model()

    def _load_matrix(self) -> sparse.csr_matrix:
        """
        Loads the matrix from cloud storage and returns it as a sparse CSR matrix.
        """
        file_content: bytes = self.cloud.download(self.matrix_name)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file.close()
            local_file_path: str = temp_file.name

        matrix: sparse.csr_matrix = sparse.load_npz(local_file_path)
        return matrix

    def _load_model(self) -> Any:
        """
        Loads the model from cloud storage and returns it.
        """
        file_content: bytes = self.cloud.download(self.model_name)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file.close()
            local_file_path: str = temp_file.name

        with open(local_file_path, 'rb') as file:
            model: Any = pickle.load(file)
        return model

    def _get_neighbors(self,
                       movie_name: str) -> tuple:
        """
        Retrieves the neighbors of a movie based on its name.
        :param movie_name:
        :return:
        """
        movie_search = self.movies[self.movies['title'].str.contains(movie_name, case=False)]
        movie_id = movie_search.iloc[0]['movieId']
        movie_id = self.preferences[self.preferences['movieId'] == movie_id].index[0]

        distances, movie_ids = self.model.kneighbors(self.csr_matrix[movie_id], n_neighbors=self.recommend_number + 1)
        return distances, movie_ids

    def _transform(self,
                   movie_name: str) -> list:
        """
        Transforms the movie name into a list of recommended movie IDs and distances.
        :param movie_name:
        :return:
        """
        distances, movie_ids = self._get_neighbors(movie_name=movie_name)
        movie_ids_list = movie_ids.squeeze().tolist()
        distances_list = distances.squeeze().tolist()
        id_dist = list(zip(movie_ids_list, distances_list))
        id_dist = sorted(id_dist, key=lambda x: x[1], reverse=False)[1:]
        return id_dist

    def recommendation(self,
                       movie_name: str) -> list[dict]:
        """
        Generates a list of movie recommendations based on the input movie name.
        :param movie_name:
        :return:
        """
        recommendations = []
        try:
            id_dist = self._transform(movie_name=movie_name)
            for ind_dist in id_dist:
                matrix_movie_id = self.preferences.iloc[ind_dist[0]]['movieId']

                ident = self.movies[self.movies['movieId'] == matrix_movie_id].index
                title = self.movies.iloc[ident]['title'].values[0]
                recommendations.append(title)
                logger.info(message.rec_found_movie.format(movie_name))
        except IndexError:
            logger.info(message.no_rec_movie.format(movie_name))
        except TypeError:
            logger.info(message.wrong_movie_type.format(str(movie_name)))
        return recommendations

