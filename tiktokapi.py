from typing import Protocol
from abc import abstractmethod

class TiktokApi(Protocol):
    @abstractmethod
    def search(self, tiktok_url : str) -> str:
        raise NotImplementedError

    @abstractmethod
    def dowload(self, download_url : str) -> bytes:
        raise NotImplementedError