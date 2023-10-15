#!/usr/bin/env python

import whisper
import sys


def transcribe(mp3_filename : str) -> str:
    mp3_filename = mp3_filename.strip()
    txt_filename = "".join(mp3_filename.split(".")[:-1]) + ".txt"

    model = whisper.load_model("base")
    result = model.transcribe(mp3_filename)

    with open(txt_filename, 'w') as f:
        f.write(result["text"])
    
    print(result["text"])

    return txt_filename


if __name__ == "__main__":
    for mp3_filename in sys.stdin:
        text_filepath = transcribe(mp3_filename)
        print(text_filepath)