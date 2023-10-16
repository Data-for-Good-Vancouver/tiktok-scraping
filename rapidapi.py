#!/usr/bin/env python

import tiktokapi
import requests
import uuid
import sys
import os
from dotenv import load_dotenv
import env
import logging

class RapidApi():

    RAPIDAPI_URL = "https://tiktok-video-no-watermark2.p.rapidapi.com/"

    def __init__(self, apikey: str = None, download_path: str = "data") -> None:
        super().__init__()

        self.download_path = download_path

        if apikey is None:
            apikey = os.getenv("RAPIDAPI_KEY")
            if apikey is None:
                logging.error("Missing API KEY")
                raise Exception("Missing API KEY")

        self.apikey = apikey

    def _headers(self) -> dict:
        return {
            "X-RapidAPI-Key": self.apikey,
            "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
        }

    def _querystring(self, tiktok_url) -> dict:
        return { "url" : tiktok_url, "hd" : "1" }

    def retrieve_video_link(self, tiktok_url: str) -> str:
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
        download_link = self.retrieve_video_link(tiktok_url)
        
        video_bytes = self.download(download_link)
        
        download_path = self.save(video_bytes)

        return download_path

if __name__ == "__main__":
    load_dotenv()
    env.setup_logging()

    api = RapidApi()

    for line in sys.stdin:
        tiktok_link = line.strip()

        if len(tiktok_link) == 0:
            continue

        download_filepath = api.get(tiktok_url=tiktok_link)

        print(download_filepath)