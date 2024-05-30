from abc import ABC, abstractmethod

import dropbox
from src.core.settings import Endpoints


class CloudStorage(ABC):
    @abstractmethod
    def upload(self, *args, **kwargs):
        pass

    @abstractmethod
    def download(self, *args, **kwargs):
        pass


class Dropbox(CloudStorage):
    def __init__(self):
        DROPBOX_ACCESS_TOKEN = Endpoints().DROPBOX_ACCESS_TOKEN
        self.dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

    def upload(self,
               local_path: str,
               remote_path: str) -> None:
        """
        Uploads a file from the local path to the remote path in Dropbox.
        :param local_path:
        :param remote_path:
        :return:
        """
        with open(local_path, 'rb') as file:
            self.dbx.files_upload(file.read(), remote_path)

    def download(self,
                 remote_path: str) -> bytes:
        """
        Downloads a file from the remote path in Dropbox.
        :param remote_path:
        :return:
        """
        response = self.dbx.files_download(remote_path)
        file_content = response[1].content
        return file_content
