#!/usr/bin/env python

import speech_recognition as sr
from os import path
from pydub import AudioSegment
import sys

if __name__ == "__main__":
    for mp3_filename in sys.stdin:
        mp3_filename = mp3_filename.strip()

        wav_filename = "".join(mp3_filename.split(".")[:-1]) + ".wav"
        
        # convert mp3 file to wav                                                       
        sound = AudioSegment.from_mp3(mp3_filename)
        sound.export(wav_filename, format="wav")

        # transcribe audio file                                                         
        AUDIO_FILE = wav_filename

        # use the audio file as the audio source                                        
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file                  

            text = r.recognize_google(audio)

            txt_filename = "".join(mp3_filename.split(".")[:-1]) + ".txt"
            with open(txt_filename, 'w') as fs:
                fs.write(text)

            print(text)