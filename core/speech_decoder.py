from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

import os
import pyaudio
import wave
import audioop
from collections import deque
import time
import math


class SpeechDetector:
    def __init__(self):
        # Microphone stream config.
        self.CHUNK = 1024  # CHUNKS of bytes to read each time from mic
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000

        self.SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
                           # only silence is recorded. When this time passes the
                           # recording finishes and the file is decoded

        self.PREV_AUDIO = 0.5  # Previous audio (in seconds) to prepend. When noise
                          # is detected, how much of previously recorded audio is
                          # prepended. This helps to prevent chopping the beginning
                          # of the phrase.

        self.THRESHOLD = 4500
        self.num_phrases = -1

        # These will need to be modified according to where the pocketsphinx folder is
        # MODELDIR = "/usr/local/lib/python3.5/dist-packages/pocketsphinx/model"
        # DATADIR = "/usr/local/lib/python3.5/dist-packages/pocketsphinxt/data"

        # Create a decoder with certain model
        config = Decoder.default_config()
        # config.set_string('-hmm', os.path.join(MODELDIR, 'en-us/en-us'))
        # config.set_string('-lm', os.path.join(MODELDIR, 'en-us/en-us.lm.bin'))
        # config.set_string('-dict', os.path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))

        # get current directory
        current_dir = os.path.dirname(os.path.realpath(__file__))

        config.set_string('-hmm', os.path.join(current_dir, "."))
        config.set_string('-lm', os.path.join(current_dir, "mk.lm"))
        config.set_string('-dict', os.path.join(current_dir, "mk.dic"))

        # Creaders decoder object for streaming data.
        self.decoder = Decoder(config)


    # def decode_phrase(self, wav_file):
    #     self.decoder.start_utt()
    #     stream = open(wav_file, "rb")
    #     while True:
    #       buf = stream.read(1024)
    #       if buf:
    #         self.decoder.process_raw(buf, False, False)
    #       else:
    #         break
    #     self.decoder.end_utt()
    #     words = []
    #     [words.append(seg.word) for seg in self.decoder.seg()]
    #     return words

    def decode_phrase(self, wav_file):
        self.decoder.start_utt()

        stream = wav_file
        while True:
          buf = stream.read(1024)
          if buf:
            self.decoder.process_raw(buf, False, False)
          else:
            break
        self.decoder.end_utt()
        words = []
        [words.append(seg.word) for seg in self.decoder.seg()]
        return words

    def run(self, wav_file):
        """
        Listens to Microphone, extracts phrases from it and calls pocketsphinx
        to decode the sound
        """
        # get current directory
        current_dir = os.path.dirname(os.path.realpath(__file__))

        r = self.decode_phrase(wav_file)
        for i in r:
        	print "DETECTED: ", i.decode('utf-8')

        print "* Done listening"

if __name__ == "__main__":
    sd = SpeechDetector()
    sd.run()