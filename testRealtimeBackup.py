import time
from pydub import AudioSegment
import pyaudio
import threading

from math import log, ceil, floor
import os
import re
from subprocess import Popen, PIPE
import sys
from tempfile import TemporaryFile
from warnings import warn
from glob import glob
from pydub import AudioSegment


def make_chunks(audio_segment, chunk_length):
    """
    Breaks an AudioSegment into chunks that are <chunk_length> milliseconds
    long.
    if chunk_length is 50 then you'll get a list of 50 millisecond long audio
    segments back (except the last one, which can be shorter)
    """
    number_of_chunks = ceil(len(audio_segment) / float(chunk_length))
    return [audio_segment[i * chunk_length:(i + 1) * chunk_length]
            for i in range(int(number_of_chunks))]


def _play_with_pyaudio(playlist):
    global state;
    state=[False,False,False,False];
    #threading.Timer(7, pauseTime).start();
    p = pyaudio.PyAudio()
     
    # break audio into half-second chunks (to allows keyboard interrupts)
    iterator=0
    #return chunk
    while iterator < len(playlist):
      seg=playlist[iterator];
      counter=0
      #threading.Timer(15, setTimesUp).start()
      #threading.Timer(20, setReplaySong).start()
    
      stream = p.open(format=p.get_format_from_width(seg.sample_width),
                    channels=seg.channels,
                    rate=seg.frame_rate,
                    output=True)
    
      for chunk in make_chunks(seg,1000):
           #if (timesUp == 1):
              # stream=stream-100;
               #timesUp=1;
           #chunk=process(chunk)
           chunk = chunk + (1* counter - 40)
           print "counter: ", counter
           #reset state variables: timesUp, skip, pause
           counter=counter+1;

           if (state[3]):
               print "nextSong"
               state=[False,False,False,False]
               break;
           elif(state[2]):
               print "replaySong!"
               iterator=iterator-1;
               state=[False,False,False,False]
               break;
           
           elif(state[0]):
               print "previousSong!"
               iterator = iterator-2;
               state=[False,False,False,False]
               break; 
           elif(state[1]):
               while (pause):
                  x=0
    
           stream.write(chunk._data)
      stream.stop_stream()
      stream.close()

      iterator=iterator+1;
    p.terminate()


def play(playlist):
      #import pyaudio
      _play_with_pyaudio(playlist)

def main():

   global state;
   state = [False, False, False, False];
   
   playlist = [AudioSegment.from_mp3(mp3_file) for mp3_file in glob("*.mp3")]


   #song = AudioSegment.from_mp3("neverGonnaGiveYouUp.mp3")

   play(playlist)


if __name__ == '__main__':
   main()

