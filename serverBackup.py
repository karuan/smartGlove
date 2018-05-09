# server.py

import socket
import select
import settings

# testRealtime.py
#import settings
#import server
import time
from pydub import AudioSegment
import pyaudio
from threading import Thread

from math import log, ceil, floor
import os
import re
from subprocess import Popen, PIPE
import sys
from tempfile import TemporaryFile
from warnings import warn
from glob import glob
from pydub import AudioSegment





def splitFun(isServer):
   global state;
   state=[0,0,0,0] 
   def serverFun():
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

      def recv_and_parse(sock): 
          try:
              data = sock.recvfrom(BUF_SIZE)[0]
              msgs = data.strip(MSG_END).split(MSG_END) 	# split messages
              ret_msgs = list()
              for msg in msgs:
                  s = msg.split(DELIM) 					# split team num and command
                  if len(s) != 4:
                      print "packet malformed: " , s
                      continue
                  
                  ret_msgs.append(s) 			# packed into tuples
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
          # this will block until at least one socket is ready
          r_ready_socks,_,_ = select.select(client, [], [])
          for sock in r_ready_socks:
              msgs = recv_and_parse(sock) # This is will not block
              print "msgs:",msgs
              state[0]=(int(msgs[0][0]))
              state[1] = (int(msgs[0][1]))
              state[2] = (int(msgs[0][2]))
              state[3] = (int(msgs[0][3]))
              print "serverState: ", state 
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
       #threading.Timer(7, pauseTime).start();
       p = pyaudio.PyAudio()
        
       # break audio into half-second chunks (to allows keyboard interrupts)
       iterator=0
       #return chunk
       while (True):
         if iterator >= len(playlist):
            iterator=0;
         if iterator<0:
            iterator=0
         seg=playlist[iterator];
         counter=0
         #threading.Timer(15, setTimesUp).start()
         #threading.Timer(20, setReplaySong).start()
         volume=0; 
         stream = p.open(format=p.get_format_from_width(seg.sample_width),
                       channels=seg.channels,
                       rate=seg.frame_rate,
                       output=True)
         pause=0; 
         for chunk in make_chunks(seg,1000):
              #if (timesUp == 1):
                 # stream=stream-100;
                  #timesUp=1;
              #chunk=process(chunk)
              chunk = chunk + volume
              print "counter: ", counter
              #reset state variables: timesUp, skip, pause
              counter=counter+1;
              print "audioState:", state
              state;
              if (state[0]==1 and state[1]==1):
                  volume=volume+2;
              elif (state[2]==1 and state[3]==1):
                  volume=volume-2;
              elif (state[3]==1):
                  print "nextSong"
                  break;
              elif(state[2]==1):
                  print "replaySong!"
                  iterator=iterator-1;
                  break;
              elif(state[0]==1):
                  print "previousSong!"
                  iterator = iterator-2;
                  break; 
              elif(state[1]==1):
                  if (pause>0):
                     pause=pause-1
                  else: 
                     while (True):
                        time.sleep(2);
                        if state[1]==1:
                           pause=2;
                           break;
              stream.write(chunk._data)
         stream.stop_stream()
         stream.close()

         iterator=iterator+1;
       p.terminate()


   def play(playlist):
         #import pyaudio
         _play_with_pyaudio(playlist)
   
   def mainFun():
      settings.init();
   
      playlist = [AudioSegment.from_mp3(mp3_file) for mp3_file in glob("*.mp3")]


      #song = AudioSegment.from_mp3("neverGonnaGiveYouUp.mp3")

      play(playlist)
   if isServer==0:
      mainFun()
   else:
      serverFun()

def main():   
  #threading.Timer(5, serverFun).start()
   thread1 = Thread(target=splitFun, args=(0,))
   
   thread1.start()
   thread2 = Thread(target=splitFun, args=(1,))
   
   thread2.start()
 


if __name__ == '__main__':
   main()


