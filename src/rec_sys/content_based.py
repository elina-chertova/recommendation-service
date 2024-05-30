import io
import tempfile

import numpy as np
import pandas as pd

from src.core.logger import logger
from src.core.messages import message
from src.rec_sys.base import RecSystem
from src.utils.cloud import Dropbox


class ContentBased(RecSystem):
    def __init__(self):
        self.cloud = Dropbox()
        self.df = pd.read_csv(io.BytesIO(self.cloud.download('/titles.csv')), index_col=0)
        self.indices = pd.Series(self.df.index)
        self.cos_sim = self._load_model()

    def _load_model(self) -> np.ndarray:
        """
        Load model to predict rec movies.
        :return:
        """
        file_content = self.cloud.download('/cos_sim.npy')
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file.close()
            local_file_path = temp_file.name
        cos_sim = np.load(local_file_path)
        return cos_sim

    def recommendation(self,
                       title: str) -> list:
        """
        Get recommendations.
        :param title:
        :return:
        """
        recommended_movies = []
        try:
            idx = self.indices[self.indices.str.contains(title, case=False)].index[0]
            score_series = pd.Series(self.cos_sim[idx]).sort_values(ascending=False)
            top_10_indexes = list(score_series.iloc[1:11].index)
            for i in top_10_indexes:
                recommended_movies.append(list(self.df.index)[i])
        except IndexError:
            logger.info(message.no_movie)
        except TypeError:
            logger.info(message.wrong_movie_type.format(str(title)))
        return recommended_movies

