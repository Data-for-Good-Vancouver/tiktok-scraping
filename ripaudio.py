#!/usr/bin/env python

from moviepy.editor import *
import sys

if __name__ == "__main__":
    original_stdout = sys.stdout
    
    for video_filename in sys.stdin:
        video_filename = video_filename.strip()
        # wrap in try catch and log (in sql for retry/debugging) the failed filename
        name = "".join(video_filename.split(".")[:-1])
        audio_filename = name + ".mp3"
        
        video = VideoFileClip(video_filename)
        sys.stdout = sys.stderr
        video.audio.write_audiofile(audio_filename)

        sys.stdout = original_stdout
        print(audio_filename)