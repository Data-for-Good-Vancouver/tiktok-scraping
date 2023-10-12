from typing import Protocol
from abc import abstractmethod

# TODO: create docs about this file: should be used as an interface/contract about other api
#       functionalities (e.g. RapidAPI vs our own future implementations)

class TiktokApi(Protocol):
    @abstractmethod
    def search(self, tiktok_url : str) -> str:
        raise NotImplementedError

    @abstractmethod
    def dowload(self, download_url : str) -> bytes:
        raise NotImplementedError