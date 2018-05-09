##this code is meant to test host.py
import socket
import sys
import time
import mraa

touch1 = mraa.Gpio(23);
touch2 = mraa.Gpio(27);
touch3 = mraa.Gpio(31);
touch4 = mraa.Gpio(33);

touch1.dir(mraa.DIR_IN);
touch2.dir(mraa.DIR_IN);
touch3.dir(mraa.DIR_IN);
touch4.dir(mraa.DIR_IN);

# server info
#SERVER_IP = "10.104.127.127" # might need to change based on the server's ip
SERVER_IP = "192.52.164.99"
PORT = 5000
 

# message format
# misc.
BUF_SIZE = 1024
sock = None

# return 0 on success, -1 on failure
def handshake(target_ip=SERVER_IP):
    global sock
    if sock == None:
        sock = socket.socket()

        sock.settimeout(5)
        try:
            sock.connect((target_ip,PORT))
            sock.send("1")
        except socket.timeout:
            print("Could not connect to server at %s:%d" % (target_ip, PORT))
            sock = None
            return -1
        print("Handshake success")
        sock.setblocking(0) # non-blocking    
        return 0
    else:
        print("Socket already connected")
        return 0

# call to broadcast STOP command
def send_stop():
    message = str(touch1.read())+","+str(touch2.read())+","+str(touch3.read())+","+str(touch4.read())+"!"
    sock.send(message)
    time.sleep(.5)
    # call on exit
def close():
    sock.close()

handshake(SERVER_IP)
while 1:
    send_stop()
