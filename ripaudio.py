#!/usr/bin/env python

from moviepy.editor import *
import sys

class Wrapper(object): # TODO: complete to wrap this and never have random stdout ouput anymore
    def __init__(self, wrapped_class, *args, **kwargs):
        self.original_stdout = sys.stdout
        # TEST
        import pprint
        pprint.pprint(args)
        pprint.pprint(kwargs)
        print("=" * 300)
        # TEST END
        self.wrapped_class = wrapped_class(*args, *kwargs)

    def __getattr__(self,attr):
        orig_attr = self.wrapped_class.__getattribute__(attr)
        if callable(orig_attr):
            def hooked(*args, **kwargs):
                self.pre()
                result = orig_attr(*args, **kwargs)
                # prevent wrapped_class from becoming unwrapped
                if result == self.wrapped_class:
                    return self
                self.post()
                return result
            return hooked
        else:
            return orig_attr

    def pre(self):
        sys.stdout = sys.stderr

    def post(self):
        sys.stdout = self.original_stdout


def rip_audio(video_filename : str) -> str:
    """
    Extracts the audio from a video file and saves it as an MP3 audio file.

    Args:
        video_filename (str): The filename of the input video file.

    Returns:
        str: The filename of the extracted audio file in MP3 format.

    This function takes a video file as input, extracts the audio from it, and saves it as an MP3 audio file with the same name as the input video file (excluding the extension).

    Example:
    >>> rip_audio("my_video.mp4")
    'my_video.mp3'
    """

    name = "".join(video_filename.split(".")[:-1])

    audio_filename = name + ".mp3"
    
    video = VideoFileClip(video_filename)

    original_stdout = sys.stdout

    sys.stdout = sys.stderr
    video.audio.write_audiofile(audio_filename)
    sys.stdout = original_stdout

    return audio_filename
    

if __name__ == "__main__":
    for video_filename in sys.stdin:
        video_filename = video_filename.strip()
        audio_filename = rip_audio(video_filename)
        print(audio_filename)