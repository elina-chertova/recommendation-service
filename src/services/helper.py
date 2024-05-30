import re

from src.rec_sys.content_based import ContentBased
from src.rec_sys.item_based import ItemBased


class ItemHelper(ItemBased):
    @staticmethod
    def remove_pattern_from_list(lst: list,
                                 pattern=r"\s*\(\d{4}\)$") -> list:
        """
        Removes a pattern from each item in a list using regular expressions.
        :param lst:
        :param pattern:
        :return:
        """
        return [re.sub(pattern, '', item) if re.search(pattern, item) else item for item in lst]

    def get_recommendation(self,
                           titles: list[str]) -> list:
        """
        Generates recommendations based on the specified titles.
        :param titles:
        :return:
        """
        result = [rec for title in titles if (rec := self.recommendation(title)) is not None]
        flattened_list = [item for sublist in result for item in sublist]
        updated_list = self.remove_pattern_from_list(flattened_list)
        return updated_list


class ContentHelper(ContentBased):
    def get_recommendation(self,
                           title: str):
        """
        Generates recommendations based on the specified titles.
        :param title:
        :return:
        """
        rec = self.recommendation(title)
        if rec:
            return rec
        return None
