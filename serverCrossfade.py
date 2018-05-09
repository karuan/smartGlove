# server.py

import socket
import select
#import settings

# testRealtime.py
#import settings
#import server
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








HOST = '192.52.164.99'                 # Symbolic name meaning all available interfaces
PORT = 5000              # Arbitrary non-privileged port
NUM_CLIENTS = 1
MAX_TEAM_NO = 2


# message format
DELIM = ","
MSG_END = "!"
MSG_TEMP = "%s" + DELIM + "%s" + MSG_END

BUF_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client = [0]

s.bind((HOST, PORT))
s.listen(1)

global state;

def recv_and_parse(sock):
    try:
        data = sock.recvfrom(BUF_SIZE)[0]
        msgs = data.strip(MSG_END).split(MSG_END) 	# split messages
	ret_msgs = list()
	for msg in msgs:
            s = msg.split(DELIM) 					# split team num and command
            if len(s) != 1:
                print "packet malformed: " , s
                continue
            
            ret_msgs.append(s[0]) 			# packed into tuples
        return ret_msgs
            
    except socket.error:
	print("No data found")
	return None

def check_socks(socks):
    print socks
    for sock in socks:
        r,_,_ = select.select([sock],[],[],0)
        print r
        if r:
            print "found dead socket: ", r ," removing now"
            socks.remove(r)

            
##handshake
print "listening for connections"
conn, addr = s.accept()
message = conn.recv(1024)
print "Connected by", addr
client= [conn]
    


while True:
    global state;
    # this will block until at least one socket is ready
    r_ready_socks,_,_ = select.select(client, [], [])
    for sock in r_ready_socks:
        msgs = recv_and_parse(sock) # This is will not block
        #state[0]=(msgs[0]%10 == 1)
        #state[1] = ((msgs[0]%100)/10 == 1)
        #state[2] = ((msgs[0]%1000)/100 == 1)
        #state[3] = (msgs[0]%1000 == 1)
        print "received message:", msgs, "from: ", sock
        if msgs is None:
            print "received empty packet"
            continue
conn.close()


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
   settings.init();
   
   playlist = [AudioSegment.from_mp3(mp3_file) for mp3_file in glob("*.mp3")]


   #song = AudioSegment.from_mp3("neverGonnaGiveYouUp.mp3")

   play(playlist)


if __name__ == '__main__':
   main()


