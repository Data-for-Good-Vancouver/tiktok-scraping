#!/usr/bin/env python

import tiktokapi
import requests
import uuid
import sys
import os
from dotenv import load_dotenv

class RapidApi():

    RAPIDAPI_URL = "https://tiktok-video-no-watermark2.p.rapidapi.com/"

    def __init__(self, apikey: str, download_path: str = "data") -> None:
        super().__init__()

        self.apikey = apikey
        self.download_path = download_path

    def _headers(self) -> dict:
        return {
            "X-RapidAPI-Key": self.apikey,
            "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
        }

    def _querystring(self, tiktok_url) -> dict:
        return { "url" : tiktok_url, "hd" : "1" }

    def search(self, tiktok_url: str) -> str:
        response = requests.get(self.RAPIDAPI_URL, headers=self._headers(), params=self._querystring(tiktok_url))

        return response.json()["data"]["play"]

    def download(self, download_url: str) -> bytes:
        response = requests.get(download_url)
        return response.content
    
    def save(self, video_bytes: bytes) -> None:
        download_filepath = os.path.join(self.download_path, str(uuid.uuid4())) + ".mp4"
        with open(download_filepath, 'wb') as fd:
            fd.write(video_bytes)
        
        return download_filepath

    def get(self, tiktok_url: str) -> str:
        """
        Downloads the tiktok video given via params.

        Args:
            tiktok_url (str): url to the actual page of the tiktok video

        Returns:
            str: downloaded video filepath
        """
        download_link = self.search(tiktok_url)
        
        video_bytes = self.download(download_link)
        
        download_path = self.save(video_bytes)

        return download_path

if __name__ == "__main__":
    load_dotenv()

    default_tiktok_link = "https://www.tiktok.com/@freshdailyvancouver/video/7232154653176188165"

    # TODO: use stdin

    apikey = os.getenv("RAPIDAPI_KEY")
    if apikey is None:
        print("[ERROR] Missing API KEY", file=sys.stderr)
        raise Exception("[ERROR] Missing API KEY")

    api = RapidApi(apikey)

    download_filepath = api.get(default_tiktok_link)

    print(download_filepath)